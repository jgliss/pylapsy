# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

with open('README.md') as file:
    readme = file.read()

with open("VERSION") as f:
    version = f.readline()
    f.close()

#with open(join("geonum","local_topo_data", "LOCAL_TOPO_PATHS.txt"), 'w'): pass

setup(
    name        =   'pylapsy',
    version     =   version,
    author      =   'Jonas Gliss',
    author_email=   'jonasgliss@gmail.com',
    license     =   'GPL-3.0',
    url         =   'https://github.com/jgliss/pylapsy',
    package_dir =   {'pylapsy'     :   'pylapsy'},
    packages    =   find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data    =   True,
    package_data=   {},
    install_requires  =   [],
    extras_require={},

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.,
        'Programming Language :: Python :: 3'
    ],

    #dependency_links    =   ["https://github.com/tkrajina/srtm.py/archive/v.0.3.1.zip#egg=srtm"],
    #package_data={'geonum':['suppl/*.dat']},
    description = 'Python toolbox for timelapse image processing',
    long_description = readme,
    entry_points = {'console_scripts' : ['ply=timelapsy.scripts.cli']},
)
