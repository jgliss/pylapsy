# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2

from pylapsy import utils, helpers
from pylapsy._lowlevel_helpers import CallableDict
from pylapsy.exceptions import ImageDimensionError
from pylapsy.image_meta_data import ImageMetaData

class Image(object):
    """pylapsy Image class
    
    Attributes
    ----------
    meta : ImageMetaData
        dict-like object containing image meta information
    
    edit_log : CallableDict
        dict-like object containing editing information
        
    Parameters
    ----------
    input 
        input image data (e.g. file path or numpy array)
    **meta
        meta information
    """
    def __init__(self, input=None, **meta):
        
        self._img = None
        
        self.meta = ImageMetaData(acq_time = np.nan,
                                  file_path = None,
                                  shape = self._get_shape,
                                  dtype = self._get_dtype)
        
        self.edit_log = CallableDict(pyrlevel = 0,
                                     gauss_blur = 0, 
                                     is_gray = self._is_gray,
                                     is_color = self._is_color)
        
        if input is not None:
            self.load_input(input)
        self.update_meta(**meta)
        
    @property
    def img(self):
        """Image data array
        
        Image data needs to be numpy array, either with 3 or 2 dimensions.
        
        Raises
        ------
        AttributeError
            if no image data is assigned to this object
        """
        if not isinstance(self._img, np.ndarray):
            raise AttributeError('Image object does not contain image data')
        return self._img
    
    @property
    def pyrlevel(self):
        """Current pyramid level of image"""
        return self.edit_log['pyrlevel']
    
    @property
    def shape(self):
        """shape of image array"""
        return self._get_shape()
    
    @property
    def dtype(self):
        """dtype of image array"""
        return self._get_dtype()
    
    @property
    def is_gray(self):
        """Boolean specifying wheter image is gray image."""
        return self._is_gray()
    
    @property
    def is_color(self):
        """Boolean specifying wheter image is color image."""
        return self._is_color()
    
    @property
    def file_path(self):
        """Image file path"""
        return self.meta['file_path']
    
    def update_meta(self, **meta):
        """Update meta information"""
        self.meta.update(**meta)
        
    def load_input(self, input, dtype=None):
        """Load input image data"""
        if isinstance(input, str):
            if not os.path.exists(input):
                raise ValueError('Need valid file path ...')
            img = cv2.imread(input)
            self.meta['file_path'] = input
        elif isinstance(input, np.ndarray):
            img = input 
        else:
            raise ValueError('Invalid input in Image class: need valid image '
                             'file path or loaded numpy array, got {}'
                             .format(type(input)))
        self._img = img
    
    def duplicate(self):
        """Duplicate instance of this object
        
        Returns
        -------
        Image
            duplicated instance of this object
        """
        img = Image(input=self._img, **self.meta)
        img.edit_log.update(self.edit_log)
        return img
        
    def mean(self):
        """Mean value of image data"""
        return self._img.mean()
    
    def min(self):
        """Minimum values of image data"""
        return self._img.min()
    
    def max(self):
        """Maximum value of image data"""
        return self._img.max()
    
    def to_gray(self, inplace=True):
        
        if not inplace:
            
            img = self.duplicate()
        else:
            img = self
        img._img = utils.to_gray(img.img)
        return img
    
    def load_test_img(self):
        """Loads test image"""
        self.load_input(helpers.get_test_img(1))
    
    def add(self, val, inplace=True):
        if not inplace:
            return self.duplicate().add(val)
        if isinstance(val, Image):
            if not val.shape == self.shape:
                raise ImageDimensionError('Cannot add Image: dimension '
                                          'mismatch: {} / {}'
                                          .format(self.shape, val.shape))
            self._img += val._img
            self.meta.merge_other(val.meta)
    
    def show(self, **kwargs):
        """Show image"""
        return utils.imshow(self.img, **kwargs)
    
    def save(self, path):
        """Save image to disk
        
        Parameters
        ----------
        path : str
            path and filename of image
        """
        if not utils.imsave(self.img, path):
            raise IOError('Failed to save image')
            
    def _get_shape(self):
        return self.img.shape
    
    def _get_dtype(self):
        return self.img.dtype

    def _is_gray(self):
        return True if self.img.ndim == 2 else False
    
    def _is_color(self):
        return True if self.img.ndim == 3 else False
    
    def __add__(self, val):
        return self.add(val, inplace=False)
    
    def __str__(self):
        """String representation"""
        from pylapsy._lowlevel_helpers import dict_to_str, _class_name
        s = _class_name(self)
        s += '\nMetadata: {}'.format(self.meta)
        s += '\nEdit-log:'
        s += dict_to_str(self.edit_log, indent=0)
        return s  
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.close('all')
    img = Image()
    img.load_test_img()
    
    print(img)
    
    img.show()