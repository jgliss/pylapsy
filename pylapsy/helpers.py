# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 
from numbers import Number

def isnumeric(val):
    """Check if input value is numeric
    
    Parameters
    ----------
    val
        input value to be checked
    
    Returns
    -------
    bool 
        True, if input value corresponds to a range, else False.
    """
    if isinstance(val, Number):
        return True
    return False

def load_exif_from_image_file(file_path):
    """Try load EXIF meta information from image file"""
    raise NotImplementedError('Coming soon...')

