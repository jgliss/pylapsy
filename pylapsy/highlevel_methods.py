# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 12:47:39 2020

@author: Jonas
"""
from pylapsy.io import find_image_files
from pylapsy import ImageList, Deshaker

def deshake(dir_name=None, file_pattern=None, outdir=None, 
            **deshake_args):
    
    
    files = find_image_files(dir_name, file_pattern)
    imglist = ImageList(files)
    deshaker = Deshaker(imglist)
    
    return deshaker.deshake(outdir=outdir, **deshake_args)

if __name__ == '__main__':
    
    import pylapsy as ply
    import os 
    data_dir = ply.DATADIR_DESHAKE_TEST
    
    outdir = os.path.join(data_dir, 'output_pylapsy')
    result = deshake(data_dir, outdir=outdir)