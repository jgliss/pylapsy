#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Note
----

This module is based on the repo:
    
    https://github.com/pmoret/deshake
    
It was modified for python 3 support and some of the code was moved into other
modules of timelapse_tools.
"""

import glob

def find_image_files(dir_name, file_pattern='*'):
    return glob.glob('{}/{}'.format(dir_name))

def get_test_images_deshake():
    raise NotImplementedError
    
