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
    print(os.path.basename(fp))
    
def shift_crop_all(files, matrices, crop, outdir):
    for file, matrix in zip(files, matrices):
        shift_crop_single(file, matrix, crop, outdir)
        
if __name__=="__main__":
    
    import matplotlib.pyplot as plt
    plt.close('all')
    from time import time, sleep
    from functools import partial
    import shutil
    REPEAT = 2
    DIR = "C:\\Users\\Jonas\\Jonas\\photography\\timelapse\\lrt_out\\LRT_20190504_sunset_noklevann\\"
       
    OUTDIR = "./output"
    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)
    fig, axes = plt.subplots(2,1,sharex=True, figsize=(18, 12))
    for usesmall in [1, 0]:
        
        if usesmall:
            files = ply.io.get_testimg_files_deshake()
        else:
            files = ply.io.find_image_files(DIR,file_pattern="*.jpg")[:10]
        
        ds = ply.Deshaker(files)
        
        h,w = ds.imglist.current_img.shape[:2]
        
        results = ds.find_shifts()
        
        dx, dy = results['dx'], results['dy']
        matrices = results['matrices']
        # determine image crop for output images in order to avoid black 
        # borders (based on maximum and minimum shifts)
        crop = ply.utils.get_crop(dx, dy, w, h)
        
        shift_crop_all(files, matrices, crop=crop, 
                       outdir=OUTDIR)
        
        from itertools import repeat
        
        smargs = zip(files, matrices, repeat(crop), repeat(OUTDIR))
        
        tests = {
        
            'single'           : [shift_crop_all, (files, matrices, crop, OUTDIR), []],
            #'concurrent_HL'    : [apply_concurrent_pool, (fs, ds.imglist), []],
            #'multiproc_HL'     : [apply_multiproc_pool, (fs, ds.imglist), []],
            'process_pool_mp'  : [apply_pool_starmap, (shift_crop_single, smargs), []],
            'thread_pool_mp'    : [apply_threadpool_starmap, (shift_crop_single, smargs), []],
            #'concurrent_LL'    : [apply_concurrent_pool, (fs1, files), []],
            #'multiproc_LL'     : [apply_multiproc_pool, (fs1, files), []],
            #'threading_LL'     : [apply_concurrent_threadpool, (fs1, files), []],
            #'threading_HL'     : [apply_concurrent_threadpool, (fs, ds.imglist), []]
            }
        
        for k in range(REPEAT):
            for test, (fun, fargs, results) in tests.items():
                print(test, usesmall, k)
                if isinstance(fargs[-1], ply.ImageList):
                    try:
                        assert fargs[-1]._index == -1, fargs[-1]._index
                    except AssertionError:
                        fargs[-1]._index = -1
                shutil.rmtree(OUTDIR)
                sleep(1)
                os.mkdir(OUTDIR)
                t0 = time()
                fun(*fargs)
                results.append(time() - t0)
                sleep(1)
        
        ls = '-'
        marker = 'x'
       
        ax = axes[usesmall]
        for name, info in tests.items():
            ax.plot(info[-1], marker=marker, ls=ls, markersize=10, label=name)
        
        ax.legend()
        ax.set_xlim([-0.5, REPEAT+1])
        if usesmall:
            tit = 'SMALL IMAGES: '
            ax.set_xlabel('Repetitions')
        else:
            tit = 'LARGE IMAGES: '
        ax.set_ylabel('Processing time [s]')
        ax.set_title(tit + '{} images (size : {})'
                     .format(len(files), (h, w)))
    fig.savefig('./performance_comparison_result.png')