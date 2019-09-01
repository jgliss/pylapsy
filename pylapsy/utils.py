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
    return cv2.imread(file_path)#opencv loads BGR as default

def imshow(img_arr, add_cbar=False, cbar_label=None,cmap=None, ax=None, 
           **kwargs):
    """Show image
    
    Works both for grayscale and color images. For color images, it is assumed
    that the index is ordered in BGR, i.e. that the image was read using 
    :func:`imread` (which uses :func:`cv2.imread`).
    
    Parameters
    ----------
    img_arr : ndarray
        image data
    add_cbar : bool
        if True, a color bar is added to the figure
    cbar_label : str, optional
        label of colorbar (only relevant if `add_cbar` is True)
    cmap : str, optional
        colormap that is supposed to be used
    ax : axes
        matplotlib axes instance that is supposed to be used for display
    **kwargs
        additional keyword args passed to :func:`imshow`
        
    Returns
    -------
    ax 
    """
    if ax is None:
        import matplotlib.pyplot as plt
        figh = 8
        h, w = img_arr.shape[:2]
        r = w / h
        figw = figh * r
        if add_cbar:
            figw += 3
            if cbar_label:
                figw += 1
            
        fig, ax = plt.subplots(1, 1, figsize=(figw, figh))
    else:
        fig = ax.figure
    if img_arr.ndim == 2 and cmap is None:
        cmap = 'gray'
    else:
        img_arr = img_arr[..., ::-1]
    disp = ax.imshow(img_arr, cmap=cmap, **kwargs)
    if add_cbar:
        cb = fig.colorbar(disp, ax=ax)
        if isinstance(cbar_label, str):
            cb.set_label(cbar_label)
    fig.tight_layout()
    return ax

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
    """Vertical sobel filter (wrapper for :func:`cv2.Sobel`)
    
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
    return np.uint8(np.abs(cv2.Sobel(img_arr, cv2.CV_64F, 0, 1, **kwargs)))

def apply_sobel_2d(img_arr, **kwargs): 
    """ Apply 2D sobel filter to in input gray-image
    
    Combines output of :func:`apply_sobel_hor` and :func:`apply_sobel_vert` 
    using :func:`cv2.bitwise_or` to retrieve edges in all directions.
    
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
    return cv2.bitwise_or(apply_sobel_hor(img_arr, **kwargs), 
                          apply_sobel_vert(img_arr, **kwargs))

# Find shift between 2 images (deshaking)
## OpenCV
    
def find_good_features_to_track(img_arr, plot=False, **params):
    """Wrapper for :func:`cv2.goodFeaturesToTrack`
    
    See `here <https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/
    py_shi_tomasi/py_shi_tomasi.html>`__ for more information.
    
    Parameters
    ----------
    img_arr : ndarray
        image data from suitable tracking coordinates are supposed to be 
        identified
    plot : bool
        option that plots the detected points onto the input image
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
    p0 = cv2.goodFeaturesToTrack(img_arr, **params)
    if plot:
        ax = imshow(img_arr)
        plot_feature_points(p0, ax=ax)
    return p0

def plot_feature_points(points, ax, marker='+',markersize=20, 
                        color='r', mew=3):
    """Plot feature points into image
    
    Parameters
    ----------
    points : ndarray
        feature points either retrieved using 
        :func:`find_good_features_to_track` or :func:`compute_flow_lk`
    ax : axes
        matplotlib axes instance in which the points are supposed to be 
        plotted (e.g. output of :func:`imshow`)
    marker : str
        marker that is supposed to be used to plot the points
    markersize : int
        size of markers
    color : str
        color of points
    mew : int
        marker edge width
    
    Returns
    -------
    ax 
    """
    pp = points.ravel()
    x = pp[0::2]
    y = pp[1::2]
    
    ax.plot(x, y, marker=marker, markersize=markersize, 
            color=color, ls='none')
        
    return ax

def compute_flow_lk(img1, img2, points_to_track=None, **params):
    """Method that computes optical flow using Lucas-Kanade algorithm
    
    Parameters
    ----------
    img1 : ndarray
        first image
    img2 : ndarray
        next image
    points_to_track : ndarray, optional
        feature points that are used for tracking (e.g. output of 
        :func:`find_good_features_to_track`). Uses 
        :func:`find_good_features_to_track`, if unspecified.
    **params
        additional keyword args passed to 
        :func:`cv2.calcOpticalFlowPyrLK`
    
    Returns
    -------
    ndarray
        feature points in `img1` that could be used for successful tracking 
        (corresponds to `points_to_track`)
    ndarray
        same points as found in level 2
    """
    if points_to_track is None:
        p0 = find_good_features_to_track(img1)
    else:
        p0 = points_to_track
    
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    
    params.update()
     
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(img1, img2, p0, None, 
                                           **lk_params)
    
    # Sanity check
    assert p0.shape == p1.shape 
    
    # Filter only valid point
    # Select good points
    return (p0[st==1], p1[st==1])
    
def find_affine_partial2d(p0=None, p1=None, **kwargs):
    """Find 2D affine transformation matrix
    
    Find affine transformation matrix for translation and rotation based on 
    input coordinates. Wrapper for method :func:`cv2.estimateAffinePartial2D`.
    
    Note
    ----
    Input feature points `p0` and `p1` can be retrieved from 2 images using 
    method :func:`compute_flow_lk`.
    
    Parameters
    ----------
    p0 : ndarray
        coordinates of feature points in first image
    p1 : ndarrax
        coordinates of feature points in next image
    **kwargs
        additional keyword args passed to :func:`cv2.estimateAffinePartial2D`
        
    Returns
    -------
    ndarray
        transformation matrix
    """
    return cv2.estimateAffinePartial2D(p0, p1, **kwargs)[0]
    
def find_homography(p0=None, p1=None):
    """Find homography matrix
    
    Find homography matrix based on 
    input coordinates. Wrapper for method :func:`cv2.estimateAffinePartial2D`.
    
    Note
    ----
    Input feature points `p0` and `p1` can be retrieved from 2 images using 
    method :func:`compute_flow_lk`.
    
    Parameters
    ----------
    p0 : ndarray
        coordinates of feature points in first image
    p1 : ndarrax
        coordinates of feature points in next image
    **kwargs
        additional keyword args passed to :func:`cv2.estimateAffinePartial2D`
        
    Returns
    -------
    ndarray
        transformation matrix
    """
    return cv2.findHomography(p0, p1)[0]

def find_shift(first_gray, second_gray, **feature_lk_params):
    """Find shift between two input images using lukas kanade optical flow
    
    Detects shift at suitable points to track in both images (e.g. corners)
    and based on detected shifts, finds the affine transformation that 
    can be used to shift and rotate the second image such that it matches best
    the first image
    
    Parameters
    ----------
    first_gray : ndarray
        first image (gray scale)
    second_gray : ndarray
        second image
    **feature_lk_params
        additional, optinal input keyword args passed to 
        :func:`compute_flow_lk`
    
    Returns
    -------
    
    """
    (good_this, 
     good_next) = compute_flow_lk(first_gray, 
                                  second_gray, 
                                  **feature_lk_params)
    
    m = find_affine_partial2d(good_this, good_next)
    shift = (m[0,2], m[1,2])
    da = np.arctan2(m[1,0], m[0,0])
    return (shift, da, m)

def shift_image(image, m=None):
    if m is None: # no shift
        m = np.zeros((2,3))
        m[0,0] = 1
        m[1,1] = 1

    if m.shape == (2, 3):
        m[0,2] = -m[0,2] 
        m[1,2] = -m[1,2]
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



    
            
class Deshaker(object):
    
    def __init__(self, images):
        pass
        
def to_pylapsy_image(input):
    """Convert input to instance of pylapsy.Image class
    
    Accepts valid image file path or numpy array
    """
    from pylapsy import Image
    if isinstance(input, Image):
        return input
    elif isinstance(input, np.ndarray):
        return Image(input)
    
# Sum it up: methods that do everything from reading of both images to deshaking them
def deshake(img1, img2):
    
    first = to_pylapsy_image(img1)
    second = to_pylapsy_image(img2)
    
    if not first.is_gray:
        first.to_gray(inplace=True)
    if not second.is_gray:
        second.to_gray(inplace=True)
        
    
    (shift, da, M) = find_shift(first_gray, second_gray)
    shifted = shift_image(second, M)
    return (crop_shift(first, shift, cv=True), crop_shift(shifted, shift, cv=True))

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.close('all')
    from pylapsy.helpers import get_test_img
    
    f1 = get_test_img(1)
    f2 = get_test_img(2)
    
    img1 = imread(f1)
    img2 = imread(f2)
    
    gray1 = to_gray(img1)
    gray2 = to_gray(img2)
    
    ax1 = imshow(gray1, True)
    
    imshow(apply_sobel_2d(gray1))
    
    p0 = find_good_features_to_track(gray1)
    
    (p0, p1) = compute_flow_lk(gray1, gray2, p0)
    (p1r, p0r) = compute_flow_lk(gray2, gray1)
    
    ax1 = plot_feature_points(p0, ax=ax1)
    ax1 = plot_feature_points(p1, ax=ax1, color='lime')
    
    M = find_affine_partial2d(p0, p1)
    
    print(M)