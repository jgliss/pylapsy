# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com
 
from ._init_utils import (_init_supplemental, _check_requirements,
                          _init_logger)

__version__, __dir__ = _init_supplemental()
logger, print_log = _init_logger()

CV2AVAILABLE = _check_requirements()
if not CV2AVAILABLE:
    print_log.warning('OpenCV library is not installed, most functions wont '
                      'work')
# Top-level classes
from .image import Image
from .image_meta_data import ImageMetaData

# Modules
from . import image
from . import image_meta_data
from . import io 
from . import utils
from . import helpers