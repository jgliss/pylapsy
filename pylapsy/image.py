# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2

class Image(object):
    """Image base class"""
    def __init__(self, input):
        
        self._img = None
        
        self.meta(acq_time = np.nan,
                  filepath = None)
        
        self.edit_log(pyrlevel = 0,
                      gauss_blur = 0, 
                      to_gray = False)

        self.load_input(input)
    
    @property
    def shape(self):
        """shape of image array"""
        return self._img.shape
    
    @property
    def dtype(self):
        """dtype of image array"""
        return self._img.dtype
    
    @property
    def is_gray(self):
        """Check if image is gray image."""
        if self.img.ndim == 2:
            return True
        elif self.img.ndim == 3:
            return False
        else:
            raise Exception("Unexpected image dimension %s..." % self.img.ndim)

    @property
    def is_binary(self):
        """Attribute specifying whether image is binary image."""
        return self.edit_log["is_bin"]

    @property
    def is_inverted(self):
        """Flag specifying whether image was inverted or not."""
        return self.edit_log["is_inv"]

    def load_input(input, dtype=None):
        """Load input image data"""
        if isinstance(input, str):
            if not os.path.exists(input):
                raise ValueError('Need valid file path ...')
            img = cv2.imread(input)
            self.meta['filepath'] = input
            if img.ndim == 3:
                img = img[...,::-1]
        elif isinstance(input, np.ndarray):
            img = input 
        self._img = img
    
    
    def duplicate(self):
        """Duplicate instance of this object
        
        Returns
        -------
        Image
            duplicated instance of this object
        """
        
    def to_gray(self, inplace=True):
        
        
    
    