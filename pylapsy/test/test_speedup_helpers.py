# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 12:46:21 2020

@author: Jonas
"""
import pytest
from pylapsy import speedup_helpers as sh

def test_apply_concurrent_threadpool():
    def square(a):
        return a**2
    res = sh.apply_concurrent_threadpool(square, [1,2])
    assert res == [1,4]
    
    
@pytest.mark.skip(reason='Coming soon...')
def test_find_shift_lowlevel(imgfile, ref_gray):
    pass
    
@pytest.mark.skip(reason='Coming soon...')
def test_find_shifts_fast(imgfiles, ref_gray):
    pass

if __name__=='__main__':
    test_apply_concurrent_threadpool()
    