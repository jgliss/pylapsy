# -*- coding: utf-8 -*-
#
# This module is part of pylapsy.
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com)
# GitHub: jgliss
# Email: jonasgliss@gmail.com

import pytest
import os
from pylapsy import io

def test_data_dir():
    ok = True
    try:
        io.data_dir()
    except FileNotFoundError:
        ok = False
    assert ok

def test_get_test_image():
    f1 = os.path.basename(io.get_test_img(which=1))
    f2 = os.path.basename(io.get_test_img(which=2))

    assert f1 == 'test_img1.jpg'
    assert f2 == 'test_img2.jpg'

def test_find_image_files():
    files = io.find_image_files(io.data_dir(), file_pattern='*.jpg')
    names = sorted([os.path.basename(x) for x in files])
    print(names)
    assert names == ['test_img1.jpg', 'test_img2.jpg']

    #print(io.find_image_files(io.data_dir(), req_same_type=False))

if __name__ == '__main__':
    pytest.main(['test_io.py'])
