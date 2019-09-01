# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 
import os

def data_dir():
    """Basic data directory"""
    from pylapsy import __dir__
    d = os.path.join(__dir__, 'data')
    if not os.path.exists(d):
        raise FileNotFoundError('Fatal: could not find pylapsy data directory')
    return os.path.abspath(d)

def get_testimg_files_deshake():
    from pylapsy import DATADIR_DESHAKE_TEST
    import glob
    return glob.glob('{}/*.jpg'.format(DATADIR_DESHAKE_TEST))

def get_test_img(which=1):
    """Get file path of test image shipped with installation
    
    Test images are stored in pylapsy/data dir and are named test_img<NUM>.jpg
    <NUM> can be specified via input parameter `which`.
    
    Parameters
    ----------
    which : int
        number of test image
        
    Returns
    -------
    str
        image file location
        
    Raises
    ------
    FileNotFoundError
        if installation data directory
        
    """
    import glob
    files = sorted(glob.glob('{}/test_img*.jpg'.format(data_dir())))
    idx = which - 1
    if idx > len(files):
        raise FileNotFoundError('Could not find test image no. {}. Maximum no. '
                                'of available test images is: {}'
                                .format(len(files)))
    return files[idx]

def load_exif_from_image_file(file_path):
    """Try load EXIF meta information from image file"""
    raise NotImplementedError('Coming soon...')
    
if __name__ == '__main__':
    print(get_testimg_files_deshake())
    
    

