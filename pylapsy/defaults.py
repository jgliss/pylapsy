# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 
"""
Global default settings
"""
def __init__():
    import cv2
    return dict(
            
            feature_params = dict(maxCorners = 100,
                                  qualityLevel = 0.3,
                                  minDistance = 7,
                                  blockSize = 7),
                                  
            lk_params = dict(winSize  = (15,15),
                             maxLevel = 2,
                             criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 
                                 10, 0.03))
)
   

defaults = __init__()         
