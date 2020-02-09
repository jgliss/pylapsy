# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 

import glob
import os

import numpy as np

def data_dir():
    """Basic data directory of pylapsy (containing example images)"""
    from pylapsy import __dir__
    d = os.path.join(__dir__, 'data')
    if not os.path.exists(d):
        raise FileNotFoundError('Fatal: could not find pylapsy data directory')
    return os.path.abspath(d)

def get_testimg_files_deshake():
    """Get list of images for example deshake sequence

    Returns
    -------
    list
        list with filepaths for example deshake sequence

    """
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

def find_image_files(dir_name=None, file_pattern=None, req_same_type=True):
    """Find image files in input directory
    
    Parameters
    ----------
    dir_name : str, optional
        input directory, if None, current directory is used
    file_pattern : str
        glob style pattern, e.g. to specify file type (e.g. *.jpg). If None, 
        *.* is used.
    req_same_type : bool
        if True and multiple file endings are found, then an exception is 
        raised
        
    Returns
    -------
    list
        list with file paths
    """
    if file_pattern is None:
        file_pattern = '*.*'
    files = glob.glob('{}/{}'.format(dir_name, file_pattern))
    if req_same_type:
        exts = np.unique([os.path.splitext(x)[1] for x in files])
        if len(exts) > 1:
            raise ValueError('Found multiple file types: {}'.format(exts))
    return files
    
    
