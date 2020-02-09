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
import pytest

def test_isnumeric():
    assert h.isnumeric(3)
    assert not h.isnumeric('bla')

if __name__=='__main__':
    pytest.main(['test_helpers.py'])