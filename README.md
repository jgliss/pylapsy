# pylapsy

Python toolbox for timelapse image processing

## Want to contribute?

This is a project I am working on in my free time (which is not a lot). Thus, I do not have a lot of time to work on this. If you like the idea (see below) feel free to get in touch and contribute.

## Installation

Installation via pip and conda installation is coming soon. Until then, clone repo and install from scatch using:

```
python setup.py install
```

or, if you would like to change the source code or add features

```
python setup.py develop
```

if you want to change the code. Make sure to install all requirements, which are specified in
requirements.txt and environment.yml.

## Deshake a timelapse image sequence using command line tool *ply*
After installation, open a terminal, navigate to your favourite shaky timelapse image sequence and
type:

```
ply -h
```

to see help on the available commands. Then, feel free to type

```
ply deshake .
```

to run the deshaker. This will create a sub directory *pylapsy_out* in which the deshaked sequence
is stored along with a preview video.

## More ideas, things that (may) come soon (or at some point)

Collection of tools for post processing of timelapse image sequences, such as:

- deshaking of timelapse sequences :heavy_check_mark:
- motion blurring
- interpolation in time to higher framerate
- deflickering of timelapse sequences
- video rendering of timelapse sequences

### Design

Object oriented, supposedly supporting to use timelapsy as API, or CLI or
potentially also providing a simple GUI or interactive jupyter dashboards.

The idea is also, to try, whenever possible, to base on existing code such as

- https://github.com/pmoret/deshake
- https://github.com/MaxNoe/timelapse-deflicker
