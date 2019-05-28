# pylapsy

Python toolbox for timelapse image processing

## Note 

This is at a very early development stage and not ready for use at the moment.

## Seeking collaborators

This is a private project, so I do not have a lot of time to work on this. Let me know if you are interested to collaborate.

## Ideas

Collection of tools for post processing of timelapse image sequences, such as:

- deshaking of timelapse sequences
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