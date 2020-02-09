# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 
"""
Command line interface of pylapsy

@author: Jonas Gliss
"""

from argparse import ArgumentParser
import os, sys
from pathlib import Path


TASKS_AVAIL = ['deshake', 'info']

def print_info():
    print('pylapsy is an open source python software that provides post '
          'processing tools for timelapse image sequences. What you need to '
          'start is:\n\n'
          'A folder containing an image sequence (provided by) '
          'argument -d. From there, try e.g.\n\n'
          'ply deshake -d . -o output')
    
class Task(object):
    """Interface for individual tasks that can be performed
    
    Can be used to specify required CLI input arguments
    """
    TASKS_AVAIL = TASKS_AVAIL
    REQUIRES_ARGS = dict(
            
            info = None,
            deshake = ['dir', 'outdir']
    )
            
    def __init__(self, name):
        if not name in TASKS_AVAIL:
            raise ValueError('No such task available: {}\n\n'
                             'Please choose from {}'
                             .format(name, TASKS_AVAIL))
        self.name = name
        
    @property
    def requires(self):
        """CLI arguments required to perform this task"""
        return self.REQUIRES_ARGS[self.name]

def cli():
    
    p = ArgumentParser(description='Command line interface of timelapsy')

    p.add_argument('task',
                   help=('Processing task that is supposed to be performed. '
                         'Choose from: {}'.format(TASKS_AVAIL)))
    p.add_argument('-d', '--dir', default='.', 
                   help=('Input directory containing timelapse sequence. '
                         'Uses "." if unspecified'))
    p.add_argument('-o', '--outdir',  
                   help=('Output directory for processed data. If unspecified '
                         'a subdirectory "pylapsy_out" is created in current '
                         'directory.'))
    p.add_argument('--file_pattern', default='*', 
                   help=('Filename pattern used to identify image files '
                         '(e.g. *.jpg)'))
    
    args = p.parse_args()
    
    task = Task(args.task)
    
    if task.name == 'info':
        print_info()
        sys.exit()
    
    
    imgdir = Path(args.dir)
    
    outdir = args.outdir
    if outdir is None:
        outdir = 'pylapsy_out'
        if not os.path.exists(outdir):
            os.mkdir(outdir)
    outdir = Path(outdir)
    if not imgdir.exists():
        raise FileNotFoundError('Input directory does not exist: {}'
                                .format(imgdir))

    print('Haaaaa haaaaaaaa (NOTHING REALLY IMPLEMENTED YET)')
    sys.exit()
        
if __name__ == '__main__':
    
    cli()
        
        
        
    