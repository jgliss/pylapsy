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
import pylapsy.helpers as h
import pylapsy.utils as u
import numpy.testing as npt
import numpy as np

PTS_FIRST = np.array([
       [ 17., 109.],
       [381.,  91.],
       [374.,  92.],
       [321.,  92.],
       [366.,  89.],
       [344.,  92.],
       [280.,  99.],
       [230., 114.],
       [  5., 110.],
       [331.,  91.],
       [292.,  97.],
       [264., 103.],
       [239., 109.],
       [ 26., 112.],
       [388.,  91.],
       [358.,  91.],
       [247., 108.],
       [169., 125.],
       [107., 112.],
       [ 58., 205.],
       [129., 116.]], dtype=np.float32)

PTS_SECOND = np.array([
       [ 16.989529, 110.79332 ],
       [380.9367  ,  92.80478 ],
       [373.95105 ,  93.80352 ],
       [320.94406 ,  93.75303 ],
       [365.9451  ,  90.78195 ],
       [343.9468  ,  93.75843 ],
       [279.90256 , 100.728   ],
       [229.95421 , 115.69796 ],
       [  4.954919, 111.80846 ],
       [330.91702 ,  92.74003 ],
       [291.96204 ,  98.70436 ],
       [263.9561  , 104.697876],
       [238.98558 , 110.66699 ],
       [ 25.973988, 113.78592 ],
       [387.9462  ,  92.8008  ],
       [357.95322 ,  92.77889 ],
       [247.03146 , 109.67142 ],
       [168.89174 , 126.62941 ],
       [106.97268 , 113.70874 ],
       [ 57.943596, 206.76143 ],
       [128.91571 , 117.68788 ]], dtype=np.float32)

M = np.array([[ 9.99941466e-01, -3.60863560e-05, -3.12518286e-02],
              [ 3.60863560e-05,  9.99941466e-01,  1.73890521e+00]])

H = np.array([[ 9.95498980e-01, -2.23218148e-03,  2.26185456e-01],
              [-5.51166384e-04,  9.88910631e-01,  2.56712074e+00],
              [-3.35641974e-06, -3.35946049e-05,  1.00000000e+00]])

@pytest.fixture(scope='session')
def test_img1():
    return u.imread(h.get_test_img(1))

@pytest.fixture(scope='session')
def test_img2():
    return u.imread(h.get_test_img(2))

def test_imread():
    img = u.imread(h.get_test_img(1))
    assert type(img) == np.ndarray
    assert img.shape == (267, 400, 3), img.shape
    npt.assert_allclose(img.mean(), 142.634, rtol=1e-2)

def test_to_gray(test_img1):
    gray = u.to_gray(test_img1)
    assert type(gray) == np.ndarray
    assert gray.shape == (267, 400), gray.shape
    npt.assert_allclose(gray.mean(), 142.462, rtol=1e-2)

def test_apply_sobel_2d(test_img1):
    edges = u.apply_sobel_2d(u.to_gray(test_img1))
    assert type(edges) == np.ndarray
    assert edges.shape == (267, 400), edges.shape
    npt.assert_allclose(edges.mean(), 45.432, rtol=1e-2)
    
def test_find_good_features_to_track(test_img1):
    p = u.find_good_features_to_track(u.to_gray(test_img1))
    npt.assert_array_equal(p.ravel(), PTS_FIRST.ravel())

def test_compute_flow_lk(test_img1, test_img2):
    
    gray1 = u.to_gray(test_img1)
    gray2 = u.to_gray(test_img2)
    
    p0 = u.find_good_features_to_track(gray1)
    
    p01, p1 = u.compute_flow_lk(gray1, gray2, p0)
    
    npt.assert_array_equal(p0.ravel(), p01.ravel())
    npt.assert_allclose(p1, PTS_SECOND)
    
def test_find_affine_partial2d():
    npt.assert_allclose(M, u.find_affine_partial2d(PTS_FIRST, 
                                                   PTS_SECOND))
    
def test_find_homography():
    npt.assert_allclose(H, u.find_homography(PTS_FIRST, 
                                             PTS_SECOND))
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.close('all')
    
    f1 = h.get_test_img(1)
    f2 = h.get_test_img(2)
    
    img1 = u.imread(f1)
    img2 = u.imread(f2)
    
    test_imread()
    test_to_gray(img1)
    test_apply_sobel_2d(img1)
    test_find_good_features_to_track(img1)
    
    gray1 = u.to_gray(img1)
    gray2 = u.to_gray(img2)
    
    ax1 = u.imshow(gray1, True)
    
    sobel = u.apply_sobel_2d(gray1)
    
    p0 = u.find_good_features_to_track(gray1)
    
    (p01, p1) = u.compute_flow_lk(gray1, gray2, p0)
    (p1r, p0r) = u.compute_flow_lk(gray2, gray1)
    
    ax1 = u.plot_feature_points(p0, ax=ax1)
    ax1 = u.plot_feature_points(p1, ax=ax1, color='lime')
    
    M = u.find_affine_partial2d(p0, p1)
    H = u.find_homography(PTS_FIRST, PTS_SECOND)
    
    
    print(H)