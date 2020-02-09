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
                dxarr=None,
                dyarr=None,
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
        
    def find_shifts(self, ref_index=None):
        """Find shifts for all images in :attr:`imglist`
        
        Parameters
        ----------
        ref_index : int
            index of reference image in image list (shifts are computed wrt 
            that image)
            
        Returns
        -------
        dict
            dictionary containing shifts (`dxarr, dyarr`) and transformation
            matrices (`matrices`) for each image in :attr:`imglist`.
        """
        if ref_index is None:
            ref_index = 0
        imglist = self.imglist
        
        dxarr, dyarr = np.empty(len(imglist)), np.empty(len(imglist))
        matrices = np.empty((len(imglist), 2, 3))
        ref = imglist[ref_index].to_gray(inplace=False).img
        
        totnum = len(imglist)
        
        disp_each = int(totnum/10)
        
        print_log.info('Finding image shifts for {} images'.format(totnum))
        for i, img in enumerate(imglist):
            if i%disp_each == 0:
                print_log.info("{} %".format(i/totnum*100))
            gray = img.to_gray(inplace=False)
            
            (dx, dy), da, M = utils.find_shift(ref, gray.img)
            matrices[i]= M
            dxarr[i] = dx
            dyarr[i] = dy
            logger.info('Image {}, dx={:.3f} dy={:.3f}'.format(i, dx, dy))    
        
        self.results['dxarr'] = dxarr
        self.results['dyarr'] = dyarr
        self.results['matrices'] = matrices
        
        return self.results
        
    def deshake(self, outdir=None, save_images=True, 
                save_preview_video=True,
                sequence_id=None, preview_fps=24):
        """Method that deshakes images sequence and saves result
        
        Parameters
        ----------
        outdir : str, optional
            output directory. If None, a subdirectory will be created in the 
            current directory
        save_images : bool
            if True, corrected images are saved
        save_preview_video : bool
            
        """
        if sequence_id is None:
            sequence_id = 'UnkownSequence'
        if outdir is None:
            outdir = 'output_{}'.format(sequence_id)
        
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        
        imglist = self.imglist
        
        # get image width and height
        h,w = imglist.current_img.shape[:2]
        
        # Find dx and dy shifts for all images
        results = self.results
        if results['dxarr'] is None:
            results = self.find_shifts()
        
        dxarr, dyarr = results['dxarr'], results['dyarr']
        matrices = results['matrices']
        # determine image crop for output images in order to avoid black 
        # borders (based on maximum and minimum shifts)
        x0,x1,y0,y1 = utils.get_crop(dxarr, dyarr, w, h)
        
        
        clip = None
        if save_preview_video:
            wnew = x1 - x0
            hnew = y1 - y0
            videopath = os.path.join(outdir, 'preview_{}.avi'.format(sequence_id))
            clip = cv2.VideoWriter(videopath,
                             cv2.VideoWriter_fourcc('M','J','P','G'), 
                             preview_fps, (wnew, hnew))
         
        totnum = len(imglist)
        
        disp_each = int(totnum/10)
        
        print_log.info('Shifting {} images'.format(totnum))
        
        for i, img in enumerate(imglist):
            if i%disp_each == 0:
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
    
    files = ply.io.get_test_images_deshake()
    
    print(files)