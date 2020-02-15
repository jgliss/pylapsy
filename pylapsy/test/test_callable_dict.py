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
from pylapsy._lowlevel_helpers import CallableDict

def make_dict():
    return CallableDict(a = 1,
                        b = 2,
                        c = lambda : 42, #callable
                        d = -3)
@pytest.fixture
def cdict():
    return make_dict()

def test_init(cdict):
    assert sorted(list(cdict.keys())) == ['a', 'b', 'c', 'd']
    assert sum(cdict.values()) == 42
    assert CallableDict(**cdict) == cdict

def test_merge_other(cdict):

    other = CallableDict(**cdict)

    cdict.merge_other(other)
    assert sorted(list(cdict.keys())) == ['a', 'b', 'c', 'd']
    assert sum(cdict.values()) == 42

    cdict1 = CallableDict(a = 1,
                          b = 2,
                          c = lambda : 42,
                          d = 'bla')

    cdict2 = CallableDict(a = 1,
                          b = 2,
                          c = lambda : 42,
                          d = 'blub')
    cdict1.merge_other(cdict2)

    vals = list(cdict1.values())
    for val in [1, 2, 42, ['bla', 'blub']]:
        assert val in vals

if __name__ == '__main__':

    cdict1 = CallableDict(a = 1,
                          b = 2,
                          c = lambda : 42,
                          d = 'bla')

    cdict2 = CallableDict(a = 1,
                          b = 2,
                          c = lambda : 42,
                          d = 'blub')


    print(cdict1)
    print(cdict2)

    cdict1.merge_other(cdict2)

    print(cdict1)
