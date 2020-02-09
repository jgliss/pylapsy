# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 

from pylapsy import Image

import pytest

@pytest.fixture
def empty_img():
    return Image()
        
@pytest.fixture(scope='session')
def example_img():
    from pylapsy.io import get_test_img
    try:
        return Image(get_test_img())
    except:
        pytest.skip('Could not initialise example image')
        
def test_meta(empty_img, example_img):
    assert 42==42

if __name__ == '__main__':
    
    pytest.main(["test_image"])
    
    