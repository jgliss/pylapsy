# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 
import pylapsy.helpers as h
import os
def test_data_dir():
    ok = True
    try:
        h.data_dir()
    except FileNotFoundError:
        ok = False
    assert ok
    
def test_get_test_image():
    f1 = os.path.basename(h.get_test_img(which=1))
    f2 = os.path.basename(h.get_test_img(which=2))
    
    assert f1 == 'test_img1.jpg'
    assert f2 == 'test_img2.jpg'