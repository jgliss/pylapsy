# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 20:56:03 2020

@author: Jonas
"""
import os

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Pool
import pylapsy as ply

def get_file_name(imgfile):
    return os.path.basename(imgfile)

def find_shift(img, ref):
    #print(os.path.basename(imgfile))
    #img = Image(imgfile)
    gray = img.to_gray(inplace=False)
    (dx, dy), da, M = ply.utils.find_shift(ref.img, gray.img)
    return (dx, dy)

def find_shift_lowlevel(imgfile, ref):
    img = ply.utils.imread(imgfile)
    gray = ply.utils.to_gray(img)
    (dx, dy), da, M = ply.utils.find_shift(ref, gray)
    return (dx, dy)

def apply_async(func, fargs, numworkers=4):
    
    result = []
    with ProcessPoolExecutor(max_workers=numworkers) as executor:
        for res in executor.map(func, fargs):
            result.append(res)
    return result

def apply_async_thread(func, fargs, numworkers=4):
    result = []
    with ThreadPoolExecutor(max_workers=numworkers) as executor:
        for res in executor.map(func, fargs):
            result.append(res)
    return result
    
def apply_async_mp(func, fargs, numworkers=4):
    
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
    

def get_shift_single(files, ref):
    shifts = []
    for file in files:
        shifts.append(find_shift_lowlevel(file, ref))
    return shifts

if __name__=="__main__":
    
    import matplotlib.pyplot as plt
    plt.close('all')
    from time import time, sleep
    from functools import partial
    
    REPEAT = 10
    DIR = "C:\\Users\\Jonas\\Jonas\\photography\\timelapse\\lrt_out\\LRT_20190504_sunset_noklevann\\"
       
    fig, axes = plt.subplots(2,1,sharex=True, figsize=(18, 12))
    for usesmall in [1, 0]:
        
        if usesmall:
            files = ply.io.get_testimg_files_deshake()
        else:
            files = ply.io.find_image_files(DIR,file_pattern="*.jpg")[:12]
        
        ds = ply.Deshaker(files)
        
        REF = ds.imglist[0].to_gray()
        fs = partial(find_shift, ref=REF)
        fs1 = partial(find_shift_lowlevel, ref=REF.img)
        
        shifts = get_shift_single(files, REF.img)
        print(shifts[0])
        
        #res = apply_async_mp(find_shift, (ds.imglist, REF.img))
        
        #raise Exception
        reflist = [REF.img] * len(files)
        fllargs = list(zip(files, reflist))
        
        res = apply_pool_starmap(find_shift_lowlevel, fargs=fllargs)
        
        tests = {'single'           : [get_shift_single, [files, REF.img], []],
                 'concurrent_HL'    : [apply_async, (fs, ds.imglist), []],
                 'multiproc_HL'     : [apply_async_mp, (fs, ds.imglist), []],
                 'starmap_LL'       : [apply_pool_starmap, (find_shift_lowlevel,fllargs), []],
                 'concurrent_LL'    : [apply_async, (fs1, files), []],
                 'multiproc_LL'     : [apply_async_mp, (fs1, files), []],
                 'threading_LL'     : [apply_async_thread, (fs1, files), []],
                 'threading_HL'     : [apply_async_thread, (fs, ds.imglist), []]
                 }
        
        for k in range(REPEAT):
            for test, (fun, fargs, results) in tests.items():
                print(test, usesmall, k)
                if isinstance(fargs[-1], ply.ImageList):
                    try:
                        assert fargs[-1]._index == -1, fargs[-1]._index
                    except AssertionError:
                        fargs[-1]._index = -1

                t0 = time()
                res = fun(*fargs)
                results.append(time() - t0)
                assert len(res) == len(files)
                for l, sh in enumerate(shifts):
                    assert res[l] == sh
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
                     .format(len(files), REF.shape))
    fig.savefig('./performance_comparison_result.jpg')