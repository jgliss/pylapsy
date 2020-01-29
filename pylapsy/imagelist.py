# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 12:14:02 2019

@author: Jonas
"""
from pylapsy.image import Image

class ImageList(object):
    
    def __init__(self, input):
        self._images = None
        self._index = -1
        
        self.load_input(input)
    
    @property
    def totnum(self):
        """Number of files in this list"""
        return len(self._images)
    
    @property 
    def index(self):
        """Current index"""
        return self._index
    
    @property
    def current_img(self):
        """Current image (at self._index)"""
        return self.get_image(self._index)
    
    @property
    def next_image(self):
        """Next image in list"""
        return self.get_image(self._index + 1)
    
    def load_input(self, input):
        if input is None:
            input = []
        elif isinstance(input, (tuple)):
            input = [x for x in input]
        elif isinstance(input, str):
            input = [input]
        if not isinstance(input, list):
            raise ValueError('Invalid input: {}. Need list (or tuple), str '
                             'or None'.format(type(input)))
        self._images = input
        
    def valid_index(self, index):
        """Check if input index is within range of images in the list"""
        return True if -1 < index < self.totnum else False
    
    def get_image(self, index):
        """Get image data"""
        img = self._images[index]
        if not isinstance(img, Image):
            img = Image(img)
        return img
    
    def __len__(self):
        return self.totnum
    
    def __getitem__(self, val):
        """Get image at input index"""
        return self.get_image(val)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self._index += 1
        if self._index == len(self._images):
            self._index = -1
            raise StopIteration
        return self[self._index]
    
if __name__ == '__main__':
    
    import pylapsy as ply
    
    lst = ImageList(ply.helpers.get_testimg_files_deshake())
    
    for i, image in enumerate(lst):
        print(i, image.shape, image.min(), image.mean(), image.max())
        