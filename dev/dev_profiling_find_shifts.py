# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:43:40 2020

Run this via command line e.g. using pyinstrument (conda install -c conda-forge pyinstrument)

python -m pyinstrument dev_profiling_find_shifts.py

or

python -m pyinstrument dev_profiling_find_shifts.py --large 

of using cProfile

python -m cProfile -s time dev_profiling_find_shifts.py 


"""
from time import time
import pylapsy as ply
from argparse import ArgumentParser

DIR = "C:\\Users\\Jonas\\Jonas\\photography\\timelapse\\lrt_out\\LRT_20190504_sunset_noklevann\\"
NUM = 10
parser = ArgumentParser()
parser.add_argument('-l', '--large', action='store_true')
parser.add_argument('-n', '--num', type=int, default=NUM)
if __name__=="__main__":
    args = parser.parse_args()
    num = args.num
    print(num)
    print(args.large)
    
    if args.large:
        images = ply.io.find_image_files(DIR)[:num]
    else:
        images = ply.io.get_testimg_files_deshake()

    t0=time()
    imglist = ply.ImageList(images)

    ds = ply.Deshaker(imglist)
    ds.find_shifts()
    
    print('ELAPSED TIME FIND SHIFTS ({} images): {:.3} s'
          .format(len(imglist), time()-t0))