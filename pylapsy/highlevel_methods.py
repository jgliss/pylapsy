# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 

from pylapsy.io import find_image_files
from pylapsy import ImageList, Deshaker

def deshake(dir_name=None, file_pattern=None, outdir=None, **deshake_args):
    """Deshake image sequence
    
    Applies deshaking to all images (which should be part of a timelapse 
    sequence) and saves the corrected images in provided output directory.
    By default, also a preview video is created. For details see 
    :class:`Deshaker`.

    Parameters
    ----------
    dir_name : str, optional
        Image directory. If None, the current directory is used. 
        The default is None.
    file_pattern : str, optional
        Pattern used to identify images in the input directory 
        (e.g. *.jpg). The default is None.
    outdir : str, optional
        Output. The default is None.
    **deshake_args 
        Additional keyword args passed to :func:`Deshaker.deshake`
        
    """
    files = find_image_files(dir_name, file_pattern)
    imglist = ImageList(files)
    deshaker = Deshaker(imglist)
    
    deshaker.deshake(outdir=outdir, **deshake_args)

if __name__ == '__main__':
    
    import pylapsy as ply
    import os 
    data_dir = ply.DATADIR_DESHAKE_TEST
    
    outdir = os.path.join(data_dir, 'output_pylapsy')
    result = deshake(data_dir, outdir=outdir)