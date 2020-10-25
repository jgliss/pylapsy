# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 

import cv2
import numpy as np
import os

from pylapsy import utils, ImageList, logger, print_log
from functools import partial
from pylapsy.speedup_helpers import find_shifts_fast, shift_crop_list

class Deshaker(object):
    """Interface for deshaking a series of images
    
    """
    def __init__(self, imglist=None, outdir=None):
    
        self._imglist = None
        # make sure input is provided properly by going through decorator 
        # assignment method
        if imglist is not None:
            self.imglist = imglist
        self.results = None
        self._init_results()
    
    def _init_results(self):
        self.results = dict(
                dx=None,
                dy=None,
                matrices=None)
        
    @property 
    def imglist(self):
        """List of images (instance of :class:`pylapsy.ImageList`)"""
        return self._imglist
    
    @imglist.setter
    def imglist(self, val):
        if not isinstance(val, ImageList):
            val = ImageList(val) # raises error if invalid
        
        self._imglist = val
        
    def find_shifts(self, ref_index=None, parallel=True):
        """Find shifts for all images in :attr:`imglist`
        
        Parameters
        ----------
        ref_index : int
            index of reference image in image list (shifts are computed wrt 
            that image)
            
        Returns
        -------
        dict
            dictionary containing shifts (`dx, dy`) and transformation
            matrices (`matrices`) for each image in :attr:`imglist`.
        """
        if ref_index is None:
            ref_index = 0
        imglist = self.imglist
        
        ref = imglist[ref_index].to_gray(inplace=False).img
        
        if parallel:
            res = find_shifts_fast(imglist.files, ref)
            dx, dy, matrices = list(zip(*res))
        else:
            dx, dy, matrices = self._find_shifts(imglist, ref)
        
        self.results['dx'] = dx
        self.results['dy'] = dy
        self.results['matrices'] = matrices
        return self.results
    
    @staticmethod
    def _find_shifts(imglist, ref):
        
        dx, dy, matrices = [],[],[]
        totnum = len(imglist)
        
        disp_each = int(totnum/4)
       
        print_log.info('Finding image shifts for {} images'.format(totnum))
        
        for i, img in enumerate(imglist):
            if totnum > 10 and i%disp_each == 0:
                print_log.info("{} %".format(i/totnum*100))
            gray = img.to_gray(inplace=False)
            (_dx, _dy), da, M = utils.find_shift(ref, gray.img)
            
            matrices.append(M)
            dx.append(_dx)
            dy.append(_dy)
            
            logger.info('Image {}, dx={:.3f} dy={:.3f}'.format(i, _dx, _dy))    
        
        return (dx, dy, matrices)

    def deshake(self, outdir=None, ref_index=None, sequence_id=None, 
                save_preview_video=False, parallel=True):
        """Method that deshakes images sequence and saves result
        
        Parameters
        ----------
        outdir : str, optional
            output directory. If None, a subdirectory will be created in the 
            current directory
        ref_index : int, optional
            Index of reference image in sequence (all images are adjusted wrt
            to this image, defaults to 0).
        sequence_id : str, optional
            name of the sequence (for output directory)
        save_preview_video : bool
            if True, a preview video is saved (currently not working)

        """
        if sequence_id is None:
            sequence_id = 'pylapsy'
        if outdir is None:
            outdir = 'output_{}'.format(sequence_id)
        
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        
        imglist = self.imglist
        
        # get image width and height
        h,w = imglist.current_img.shape[:2]
        
        # Find dx and dy shifts for all images
        results = self.results
        if results['dx'] is None:
            results = self.find_shifts(ref_index=ref_index, 
                                       parallel=parallel)
        
        dx, dy = results['dx'], results['dy']
        matrices = results['matrices']
        # determine image crop for output images in order to avoid black 
        # borders (based on maximum and minimum shifts)
        crop = utils.get_crop(dx, dy, w, h)
        
        shift_crop_list(imglist.files, 
                                 matrices, 
                                 crop, 
                                 outdir,
                                 multiproc=parallel,
                                 multithread=False)
          
        if save_preview_video:
            raise NotImplementedError  
        
        print_log.info('Results are stored at {}'.format(outdir))
        
    def deshake_v0(self, outdir=None, ref_index=None, sequence_id=None, 
                save_images=True, save_preview_video=True,
                preview_fps=24):
        """Method that deshakes images sequence and saves result
        
        Parameters
        ----------
        outdir : str, optional
            output directory. If None, a subdirectory will be created in the 
            current directory
        ref_index : int, optional
            Index of reference image in sequence (all images are adjusted wrt
            to this image, defaults to 0).
        sequence_id : str, optional
            name of the sequence (for output directory)
        save_images : bool
            if True, corrected images are saved
        save_preview_video : bool
            if True, a preview video is saved
        preview_fps : int
            fps of preview video (if applicable)
            
            
        """
        if sequence_id is None:
            sequence_id = 'pylapsy'
        if outdir is None:
            outdir = 'output_{}'.format(sequence_id)
        
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        
        imglist = self.imglist
        
        # get image width and height
        h,w = imglist.current_img.shape[:2]
        
        # Find dx and dy shifts for all images
        results = self.results
        if results['dx'] is None:
            results = self.find_shifts()
        
        dx, dy = results['dx'], results['dy']
        matrices = results['matrices']
        # determine image crop for output images in order to avoid black 
        # borders (based on maximum and minimum shifts)
        x0,x1,y0,y1 = utils.get_crop(dx, dy, w, h)
        
        
        clip = None
        if save_preview_video:
            wnew = x1 - x0
            hnew = y1 - y0
            videopath = os.path.join(outdir, 'preview_{}.avi'.format(sequence_id))
            try:
                clip = cv2.VideoWriter(videopath,
                                 cv2.VideoWriter_fourcc('M','J','P','G'), 
                                 preview_fps, (wnew, hnew))
            except Exception as e:
                save_preview_video = False
                print_log.warning('Failed to init VideoWriter. Reason: {}'
                                        .format(repr(e)))
         
        totnum = len(imglist)
        
        disp_each = int(totnum/4)
        
        print_log.info('Shifting {} images'.format(totnum))
        
        for i, img in enumerate(imglist):
            if totnum > 10  and i%disp_each == 0:
                print_log.info("{} %".format(i/totnum*100))
            shifted = utils.shift_image(img.img, matrices[i])
            
            shifted_crop = shifted[y0:y1, x0:x1]
            
            if save_preview_video:
                clip.write(shifted_crop)
            
            if save_images:
                fp = os.path.join(outdir, os.path.basename(imglist.files[i]))
                utils.imsave(shifted_crop, fp)
        if save_preview_video:
            clip.release()
        print_log.info('Results are stored at {}'.format(outdir))

if __name__=='__main__':
    
    import pylapsy as ply
    from time import time
    DIR = "C:\\Users\\Jonas\\Jonas\\photography\\timelapse\\lrt_out\\LRT_20190504_sunset_noklevann\\"
    
    
    files = ply.io.get_testimg_files_deshake()
    
    #files = ply.io.find_image_files(DIR,file_pattern='*.jpg')
    
    
    ds = Deshaker(files)
    ds.deshake()