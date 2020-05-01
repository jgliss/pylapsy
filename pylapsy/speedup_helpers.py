# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 12:46:21 2020

@author: Jonas
"""
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool, Pool
from pylapsy import utils
from itertools import repeat
import os

def apply_concurrent_threadpool(func, iterable, numworkers=4):
    """
    Use ThreadPoolExecutor to speed up multiple calls of input function

    Parameters
    ----------
    func : callable
        first argument is iterated over, provided via input `iterable`.
    iterable : iterable
        list or similar containing first input arg for `func`
    numworkers : TYPE, optional
        Number of threads. The default is 4.

    Returns
    -------
    result : list
        list of tuples containing return values of `func` after execution with
        args in `iterable`

    """
    result = []
    
    with ThreadPoolExecutor(max_workers=numworkers) as executor:
        for res in executor.map(func, iterable):
            result.append(res)
    return result

def find_shift_lowlevel(imgfile, ref_gray):
    """
    Find shift between two images

    Parameters
    ----------
    imgfile : str
        image file read via :func:`pylapsy.utils.imread`
    ref_gray : ndarray
        reference image wrt to which shift of imgfile is retrieved

    Returns
    -------
    dx : float
        x shift
    dy : float
        y shift
    M : ndarray
        affine transformation matrix
    """
    img = utils.imread(imgfile)
    gray = utils.to_gray(img)
    (dx, dy), da, M = utils.find_shift(ref_gray, gray)
    return (dx, dy, M)

def find_shifts_fast(imgfiles, ref_gray):
    """
    Use ThreadPool to find shifts for list of images

    Parameters
    ----------
    imgfiles : list
        list containing file locations of images
    ref_gray : ndarray
        reference gray image wrt to which shifts are computed

    Returns
    -------
    list
        list of 3-element tuples containing (dx, dy, M) for each image in 
        input file list, where dx, dy denote the image shift and M is the 
        affine transformation matrix
    """
    func = partial(find_shift_lowlevel, ref_gray=ref_gray)
    return apply_concurrent_threadpool(func, imgfiles)

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
    img = utils.imread(file)
    shifted = utils.shift_image(img, matrix)
    shifted_crop = shifted[y0:y1, x0:x1]
    fp = os.path.join(outdir, os.path.basename(file))
    utils.imsave(shifted_crop, fp)

def shift_crop_list_fast(files, matrices, crop, outdir,
                         multithread=False):
    smargs = zip(files, matrices, repeat(crop), repeat(outdir))
    func = apply_threadpool_starmap if multithread else apply_pool_starmap
    func(shift_crop_single, smargs)
    
def shift_crop_list(files, matrices, crop, outdir, multiproc=True, 
                    multithread=False):
    if multiproc:
        shift_crop_list_fast(files, matrices, crop, outdir,
                                    multithread=False)
    elif multithread:
        shift_crop_list_fast(files, matrices, crop, outdir,
                                    multithread=True)
    else:
        for file, matrix in zip(files, matrices):
            shift_crop_single(file, matrix, crop, outdir)

if __name__=='__main__':
    import numpy as np
    
    def func1(a):
        return a
    
    def func2(a, b=10):
        res = a+b
        return res
    
    a = np.arange(10)

    res = apply_concurrent_threadpool(func1,a)
    res1 = apply_concurrent_threadpool(func2,a)
    
    print(res)
    print(res1)
    
    import pylapsy as ply
    
    files = ply.io.get_testimg_files_deshake()[:20]
    
    ref = ply.Image(files[0]).to_gray().img
    
    res = find_shifts_fast(files, ref)
    
    print(res)