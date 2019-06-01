# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 

class ImageDimensionError(ValueError):
    pass

class MetaDataConflict(ValueError):
    pass

class MetaMergingError(MetaDataConflict):
    pass