# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:43:40 2020

@author: Jonas
"""

import pylapsy as ply
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import time

        
plt.close('all')
images = ply.io.get_testimg_files_deshake()
#images = ply.helpers.get_testimg_files_deshake()

imglist = ply.ImageList(images)

outname = 'testvideo.avi'
outname_cc = 'testvideo_concat.avi'

if os.path.exists(outname):
    os.remove(outname)
    time.sleep(1)
if os.path.exists(outname_cc):
    os.remove(outname_cc)
    time.sleep(1)

def find_shifts(imglist, ref_index=0):
    dxarr, dyarr = np.empty(len(imglist)), np.empty(len(imglist))
    matrices = np.empty((len(imglist), 2, 3))
    ref = imglist[ref_index].to_gray(inplace=False).img
    
    for i, img in enumerate(imglist):
        gray = img.to_gray(inplace=False)
        
        (dx, dy), da, M = ply.utils.find_shift(ref, gray.img)
        matrices[i]= M
        dxarr[i] = dx
        dyarr[i] = dy
        print('Image {}, dx={:.3f} dy={:.3f}'.format(i, dx, dy))    
    
    return (dxarr, dyarr, matrices)
 
dxarr, dyarr, matrices = find_shifts(imglist)

first = imglist[0]
first_concat = np.concatenate((first.img, first.img), axis=0)
sh = first.shape

w = sh[1]
h = sh[0]
out_concat = cv2.VideoWriter(outname_cc,
                             cv2.VideoWriter_fourcc('M','J','P','G'), 
                             15, (w,h*2))

#out.write(first_concat)

x0,x1,y0,y1 = ply.utils.get_crop(dxarr, dyarr, w, h)
wnew = x1 - x0
hnew = y1 - y0
print('Previous image shape: W={}, H={}'.format(w, h))
print('Cropped image shape: W={}, H={}'.format(wnew, hnew))

out = cv2.VideoWriter(outname,
                      cv2.VideoWriter_fourcc('M','J','P','G'), 
                      15, (wnew,hnew))

#crop = [int(min(y_shift)) - 1, int(max(y_shift)) + 1, int(min(x_shift)) - 1, int(max(x_shift)) + 1]
for i, img in enumerate(imglist):
    #gray = img.to_gray(inplace=False)
    #(dx, dy), da, M = ply.utils.find_shift(ref, gray.img)
    shifted = ply.utils.shift_image(img.img, matrices[i])
    
    concat = np.concatenate((img.img, shifted), axis=0)
    
    shifted_crop = shifted[y0:y1, x0:x1]
    out_concat.write(concat)
    
    out.write(shifted_crop)
    

out.release()    
out_concat.release()
print(max(dxarr))
print(max(dyarr))

ds = ply.Deshaker(imglist)
ds.deshake()
