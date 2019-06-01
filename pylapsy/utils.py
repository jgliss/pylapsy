import cv2
import numpy as np

def imread(file_path):
    """Read image file using :func:`cv2.imread`
    
    Note
    ----
    opencv reads in BGR mode, not RGB
    
    Parameters
    ----------
    file_path : str
        image file path
        
    Returns
    -------
    ndarray
        image data
    """
    cv2.imread(file_path)#opencv loads BGR as default

# Convert to gray-scale
def to_gray(img_arr):
    """Convert image array to gray
    
    Parameters
    ----------
    img_arr : ndarray
        color image data with color indices in BGR mode (cf. :func:`imread`).
        Shape: `(N, M, 3)`
    
    Returns
    -------
    img_arr : ndarray
        gray image data (cf. :func:`imread`).
        Shape: `(N, M, 1)`
    """
    return cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)

# Detect edges (Sobel filter)
def apply_sobel_hor(img_arr, **kwargs):
    """Horizontal sobel filter (wrapper for :func:`cv2.Sobel`)
    
    Parameters
    ----------
    img_arr : ndarray
        input grayscale image
    **kwargs
        additional keyword args passed to :func:`cv2.Sobel`
    Returns
    -------
    ndarray
        filtered input image array
    """
    return np.uint8(np.abs(cv2.Sobel(img_arr, cv2.CV_64F, 1, 0, **kwargs)))

def apply_sobel_vert(img_arr, **kwargs):
    return np.uint8(np.abs(cv2.Sobel(img_arr, cv2.CV_64F, 0, 1, **kwargs)))

def apply_sobel_2d(img_arr, **kwargs): 
    """ Apply 2D sobel filter to in input gray-image
    
    Combines output of :func:`apply_sobel_hor` and :func:`apply_sobel_vert` 
    using :func:`cv2.bitwise_or` to retrieve edges in all directions.
    
    Parameters
    ----------
    img_arr : ndarray
        input grayscale image
    
    Returns
    -------
    ndarray
        filtered input image array
    """
    return cv2.bitwise_or(apply_sobel_hor(img_arr, **kwargs), 
                          apply_sobel_vert(img_arr, **kwargs))

# Find shift between 2 images (deshaking)
## OpenCV
    
def find_good_features_to_track(img_arr, **params):
    """Wrapper for :func:`cv2.goodFeaturesToTrack`
    
    See `here <https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/
    py_shi_tomasi/py_shi_tomasi.html>`__ for more information.
    
    Parameters
    ----------
    img_arr : ndarray
        image data from suitable tracking coordinates are supposed to be 
        identified
    **params
        additional input parameters that are passed to 
        :func:`cv2.goodFeaturesToTrack` 
    
    Returns
    -------
    ndarray
        list of coordinates
    """
    if not img_arr.ndim == 2:
        from pylapsy import print_log
        print_log.warning('Input should be gray-scale...')
        
    # default params
    params = dict(maxCorners = 100,
                  qualityLevel = 0.3,
                  minDistance = 7,
                  blockSize = 7)
    params.update(**params)
    return cv2.goodFeaturesToTrack(img_arr, **params)

def compute_flow_lk(first_gray, second_gray, points_to_track=None, 
                    **params):
    """Method that computes optical flow using Lucas-Kanade algorithm
    
    """
    if points_to_track is None:
        p0 = find_good_features_to_track(first_gray)
    else:
        p0 = points_to_track
    
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    
    params.update()
     
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(first_gray, second_gray, p0, None, **lk_params)
    
    # Sanity check
    assert p0.shape == p1.shape 
    
    # Filter only valid point
    # Select good points
    return (p0[st==1], p1[st==1])
    
def find_affine_partial2d(good_this=None, good_next=None, **flowlk_kwargs):
    if good_this is None:
        good_this, good_next = _compute_flow_lk(**flowlk_kwargs)
    
    #Find transformation matrix
    return cv2.estimateAffinePartial2D(good_this, good_next)[0]
    
def find_homography(good_this=None, good_next=None, **flowlk_kwargs):
    if good_this is None:
        good_this, good_next = _compute_flow_lk(**flowlk_kwargs)
    
    return cv2.findHomography(good_this, good_next)[0]

def find_shift(first_gray, second_gray, **feature_lk_params):
    good_this, good_next = _compute_flow_lk(first_gray, second_gray, **feature_lk_params)
    
    m = find_affine_partial2d(good_this, good_next)
    shift = (m[0,2], m[1,2])
    da = np.arctan2(m[1,0], m[0,0])
    return (shift, da, m)

## scikit-image
def find_shift_ski(first_gray, second_gray):
    first_edges = ski.filters.sobel(first_gray)
    second_edges =ski.filters.sobel(second_gray)
    
    shift, error, diffphase = register_translation(first_edges, second_edges, 100)
    return shift

# Shift image
def shift_image_ski(image, shift=None):
    if shift is None:
        shift = (0,0)
    dy, dx = shift
    tf_shift = ski.transform.SimilarityTransform(translation=[-dx, -dy])
    shifted = ski.transform.warp(image, tf_shift)
    return shifted

def shift_image(image, m=None):
    if m is None: # no shift
        m = np.zeros((2,3))
        m[0,0] = 1
        m[1,1] = 1

    m[0,2] = -m[0,2] 
    m[1,2] = -m[1,2]
    if m.shape == (2, 3):
        shifted = cv2.warpAffine(image, m, (image.shape[1], image.shape[0]))
    elif m.shape == (3,3):
        shifted = cv2.warpPerspective(image, m, (image.shape[1], image.shape[0]))
    else:
        raise ValueError('Invalid input for transormation matrix m')
    return shifted

def crop_shift(img, shift, cv=True):
    if cv:
        dx, dy = shift
    else:
        dy, dx = -shift[0], -shift[1]
    dx = int(round(dx))
    dy = int(round(dy))
    if img.ndim==2:
        h, w = img.shape
    else:
        h, w, _ = img.shape
    x0, y0, x1, y1 = 0,0,w,h
    if dx > 0: #second frame was shifted to the left -> crop right
        x1 = -dx-1
    elif dx < 0: # second frame was shifted to the right -> crop left
        x0 = -dx+1
    if dy > 0: #second frame was shifted to the top -> crop bottom
        y1 = -dy-1
    elif dy < 0: # second frame was shifted to the right -> crop top
        y0 = -dy+1
    return img[y0:y1, x0:x1]

# Sum it up: methods that do everything from reading of both images to deshaking them
def deshake(imfile1, imfile2):
    first = imread(imfile1)
    second = imread(imfile2)
    
    first_gray = to_gray(first)
    second_gray = to_gray(second)
    
    (shift, da, M) = find_shift(first_gray, second_gray)
    shifted = shift_image(second, M)
    return (crop_shift(first, shift, cv=True), crop_shift(shifted, shift, cv=True))