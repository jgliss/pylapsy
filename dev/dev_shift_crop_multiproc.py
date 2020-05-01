# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 20:56:03 2020

@author: Jonas
"""

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import pylapsy as ply
import os
from time import time
import glob
from itertools import repeat
from tqdm import tqdm

def apply_concurrent_pool(func, fargs, numworkers=4):
    
    result = []
    with ProcessPoolExecutor(max_workers=numworkers) as executor:
        for res in executor.map(func, fargs):
            result.append(res)
    return result

def apply_concurrent_threadpool(func, fargs, numworkers=4):
    result = []
    with ThreadPoolExecutor(max_workers=numworkers) as executor:
        for res in executor.map(func, fargs):
            result.append(res)
    return result
    
def apply_multiproc_pool(func, fargs, numworkers=4):
    
    with Pool(numworkers) as p:
        result = p.map(func, fargs)
    p.close()
    p.join()
    return result

def apply_pool_starmap(func, fargs, numworkers=4):
    
    with Pool(numworkers) as p:
        result = p.starmap(func, fargs)
    p.close()
    p.join()
    return result

def apply_pool_starmap_tqdm(func, fargs, numiter, numworkers=4):
    with Pool(numworkers) as p:
        result = list(tqdm(p.starmap(func, fargs), total=numiter))
    p.close()
    p.join()
    return result

def apply_threadpool_starmap(func, fargs, numworkers=4):
    
    with ThreadPool(numworkers) as p:
        result = p.starmap(func, fargs)
    p.close()
    p.join()
    return result    

def shift_crop_single(file, matrix, crop, outdir):
    x0,x1,y0,y1 = crop
    img = ply.utils.imread(file)
    shifted = ply.utils.shift_image(img, matrix)
    shifted_crop = shifted[y0:y1, x0:x1]
    fp = os.path.join(outdir, os.path.basename(file))
    ply.utils.imsave(shifted_crop, fp)
    
def shift_crop_all(files, matrices, crop, outdir):
    for file, matrix in zip(files, matrices):
        shift_crop_single(file, matrix, crop, outdir)
        
if __name__=="__main__":
    
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('-t', '--test', default='single')
    parser.add_argument('-n', '--num', default='20')
    
    args = parser.parse_args()
    
    test = args.test
    num = int(args.num)
    
    print('Running', test, num, 'images')

    DIR = "C:\\Users\\Jonas\\Jonas\\photography\\timelapse\\lrt_out\\LRT_20190504_sunset_noklevann\\"
       
    OUTDIR = "./output"
    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)
    
    for file in glob.glob('{}/*.jpg'.format(OUTDIR)):
        os.remove(file)
        
    files = ply.io.find_image_files(DIR,file_pattern="*.jpg")
    if len(files) < num:
        raise ValueError('input num exceeds number of available pictures',len(files))
    files = files[:num]
    
    ds = ply.Deshaker(files)
    
    h,w = ds.imglist.current_img.shape[:2]
    
    t0 =time()
    results = ds.find_shifts()
    dt = time() -t0
    print('Found shifts for {} images (in {:.1f} s)'.format(len(files), dt))
    dx, dy = results['dx'], results['dy']
    matrices = results['matrices']
    
    # determine image crop for output images in order to avoid black 
    # borders (based on maximum and minimum shifts)
    crop = ply.utils.get_crop(dx, dy, w, h)
    
    smargs = zip(files, matrices, repeat(crop), repeat(OUTDIR))
    
    tests = {
    
        'single'           : [shift_crop_all, (files, matrices, crop, OUTDIR)],
        #'concurrent_HL'    : [apply_concurrent_pool, (fs, ds.imglist), []],
        #'multiproc_HL'     : [apply_multiproc_pool, (fs, ds.imglist), []],
        'process_pool'  : [apply_pool_starmap, (shift_crop_single, smargs)],
        'process_pool_tqdm'  : [apply_pool_starmap_tqdm, (shift_crop_single, smargs, len(files))],
        'thread_pool_mp'    : [apply_threadpool_starmap, (shift_crop_single, smargs)],
        #'concurrent_LL'    : [apply_concurrent_pool, (fs1, files), []],
        #'multiproc_LL'     : [apply_multiproc_pool, (fs1, files), []],
        #'threading_LL'     : [apply_concurrent_threadpool, (fs1, files), []],
        #'threading_HL'     : [apply_concurrent_threadpool, (fs, ds.imglist), []]
        }
    
    if not test in tests:
        raise ValueError('No such test with name {}, choose from {}'
                         .format(test, list(tests.keys())))
        
    fun, fargs = tests[test]
    
    if isinstance(fargs[-1], ply.ImageList):
        try:
            assert fargs[-1]._index == -1, fargs[-1]._index
        except AssertionError:
            fargs[-1]._index = -1
    
    t0 = time()
    fun(*fargs)
    print('Elapsed time: {:.3f} s'.format(time() - t0))
    
    print('Running pylapsy default (find shifts and deshake)')
    t0 = time()
    ds.deshake(outdir=OUTDIR)
    
    print('Elapsed time: {:.3f} s'.format(time() - t0))
    
    
    