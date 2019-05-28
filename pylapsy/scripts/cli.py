# -*- coding: utf-8 -*-
"""
Command line interface of pylapsy

@author: Jonas Gliss
"""

from argparse import ArgumentParser

def tasks_available():
    return ['deshake', 'info']


if __name__ == '__main__':
    import pylapsy as ply
    
    p = ArgumentParser(description='Command line interface of timelapsy')

    p.add_argument('task',
                   help=('Processing task that is supposed to be performed'
                         'Choose from: {}'.format(tasks_available())))
    p.add_argument('-d', '--dir', default='.', 
                   help=('Input directory containing timelapse sequence'
                         'Uses "." if unspecified'))
    p.add_argument('-o', '--outdir', 
                   help=('Output directory for processed data. If unspecified '
                         'a subdirectory "lapsy_out" is created in input dir'))
    p.add_argument('--file_pattern', default='*', 
                   help=('Filename pattern used to identify image files '
                   '(e.g. *.jpg)'))
    
    from pathlib import Path
    args = p.parse_args()
    
    task = args.task
    imgdir = Path(args.dir)
    outdir = Path(args.outdir)
    if not imgdir.exists():
        raise FileNotFoundError('Input directory does not exist: {}'
                                .format(imgdir))
    
    if outdir is None:
        outdir = '.'
    
        
        
        
    