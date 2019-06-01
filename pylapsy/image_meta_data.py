# -*- coding: utf-8 -*-

from pylapsy import helpers as h
from pylapsy._lowlevel_helpers import CallableDict
 
class ImageMetaData(CallableDict):
    """Image metadata class
    
    Extended dictionary that supports dynamic value generation (i.e. if an
    assigned value is callable, it will be executed on demand) and some other
    methods. 
    """
    def load(self, file_path):
        """Load meta information from file
        
        Parameters
        ----------
        file_path : str
            image file containing meta information
        """
        self.update(h.load_exif_from_image_file(file_path))
           
if __name__ == '__main__':
    def yield_42():
        return 42
    
    meta = ImageMetaData(a = 1, 
                         b = 2, 
                         c = yield_42)
    
    print(meta)
        