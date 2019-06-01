# -*- coding: utf-8 -*-
#
# This module is part of pylapsy. 
# It is licensed under a GPL-3.0 license, for details see LICENSE file.
#
# Author: Jonas Gliß
# Copyright (C) 2019 Jonas Gliss (jonasgliss@gmail.com) 
# GitHub: jgliss
# Email: jonasgliss@gmail.com 
import numpy as np
from collections.abc import MutableMapping
from pylapsy.exceptions import MetaMergingError

def _class_name(obj):
    """Returns class name of an object"""
    return type(obj).__name__
    
def list_to_shortstr(lst, indent=0):
    """Custom function to convert a list into a short string representation"""
    if len(lst) == 0:
        return "\n" + indent*" " + "[]\n"
    elif len(lst) == 1:
        return "\n" + indent*" " + "[%s]\n" %repr(lst[0])
    s = "\n" + indent*" " + "[%s\n" %repr(lst[0])
    if len(lst) > 4:
        s += (indent+1)*" " + "%s\n" %repr(lst[1])
        s += (indent+1)*" " + "...\n"
        s += (indent+1)*" " + "%s\n" %repr(lst[-2])
    else: 
        for item in lst[1:-1]:
            s += (indent+1)*" " + "%s" %repr(item)
    s += (indent+1)*" " + "%s]\n" %repr(lst[-1])
    return s
        
def dict_to_str(dictionary, s="", indent=0):
    """Custom function to convert dictionary into string (e.g. for print)
    
    Parameters
    ----------
    dictionary : dict
        the dictionary
    s : str
        the input string
    indent : int
        indent of dictionary content
    
    Returns
    -------
    str
        the modified input string
        
    Example
    -------
    
    >>> string = "Printing dictionary d"
    >>> d = dict(Bla=1, Blub=dict(BlaBlub=2))
    >>> print(dict_to_str(d, string))
    Printing dictionary d
       Bla: 1
       Blub (dict)
        BlaBlub: 2
    
    """
    for k, v in dictionary.items():
        if isinstance(v, dict):
            s += "\n" + indent*" " + "{} ({})".format(k, type(v))
            s = dict_to_str(v, s, indent+1)
        elif isinstance(v, list):
            s += "\n" + indent*" " + "{} (list, {} items)".format(k, len(v))
            s += list_to_shortstr(v)
        elif isinstance(v, np.ndarray) and v.ndim==1:
            s += "\n" + indent*" " + "{} (array, {} items)".format(k, len(v))
            s += list_to_shortstr(v)
        else:
            s += "\n" + indent*" " + "{}: {}".format(k, v)
    return s
    
class CallableDict(MutableMapping):
    """Dictionary-like object that supports on-demand callable values
    
    Extended dictionary that supports dynamic value generation (i.e. if an
    assigned value is callable, it will be executed on demand).
    """
    # dictionary containing howto merging information for individual 
    # attributes (keys) of an instance of this class. Is used in 
    # :func:`merge_other` and may be specified in derived implementations
    _MERGERS = {}
    def __init__(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)
    
    # The next five methods are requirements of the ABC.
    def __setitem__(self, key, value):
        self.__dict__[key] = value
    
    def __getitem__(self, key):
        val = self.__dict__[key]
        if callable(val):
            return val()
        return val
    
    def __delitem__(self, key):
        del self.__dict__[key]
    
    def __iter__(self):
        return iter(self.__dict__)
    
    def __len__(self):
        return len(self.__dict__)
    
    def __repr__(self):
        '''echoes class, id, & reproducible representation in the REPL'''
        return '{}, {}({})'.format(_class_name(self),
                                   super(CallableDict, self).__repr__(), 
                                   self.__dict__)
    def __str__(self):
        s = ''
        for k, v in self.items():
            s += '\n{}: {}'.format(k, v)
        return s
    
    def merge_other(self, other):
        """Merge metadata of other metadata object into this"""
        if not isinstance(other, MutableMapping):
            raise ValueError('Need MutableMapping (dict, etc.)')
        
        # Check what the input is (classes that are dict do not have 
        # __dict__ attr., but this one here has).
        if isinstance(other, dict):
            d = other
        else:
            d = other.__dict__
        
        # Loop over the entries in the other object and merge, where possible
        for k, v in d.items():
            if not k in self:
                self.__dict__[k] = v
                continue
            elif self.__dict__[k] == v:
                # Nothing to do
                continue
            val_here = self.__dict__[k]
            
            _add_info = ('key {}: val (here)= {}, val (other): {}'.format(k, val_here, v))
            # key exists in both dictionaries
            if k in self._MERGERS: 
                # there is a particular merging method available 
                self.__dict__[k] = self._MERGERS[k](val_here, v)
            # key exists in both objects
            if callable(v):
                if not callable(val_here):
                    raise MetaMergingError('Cannot merge callable with '
                                           'non-callable value', _add_info)
                elif not val_here() == v():
                    raise MetaMergingError('Cannot merge 2 callables that '
                                           'yield different values', _add_info)
                # it is satisified that callable entry is the same in both
                # objects. Nothing to do.
                continue
            
            # key exists in both objects and is not callable in the other one
            elif callable(val_here):
                if not v == val_here():
                    raise MetaMergingError('Cannot merge non-callable with '
                                           'callable value', _add_info)
                continue
            # value in other is string (strings are the only objects that will,
            # be automatically merged into list of strings, in both directions, 
            # i.e. next 2 elif blocks)
            elif isinstance(v, str):
                if isinstance(val_here, str):
                    self.__dict__[k] = [val_here, v]
                    continue
                elif isinstance(val_here, list):
                    if not all([isinstance(x, str) for x in val_here]):
                        raise MetaMergingError('Cannot merge string into a '
                                               'list containing other values'
                                               'than strings', _add_info)
                    self.__dict__[k].append(v)
                    continue
                
            elif isinstance(v, list):
                if not all([isinstance(x, str) for x in v]):
                    raise MetaMergingError('Cannot merge list containing other '
                                           'values than strings', _add_info)
                if isinstance(val_here, str):
                    self.__dict__[k] = [val_here] + v
                    continue
                elif isinstance(val_here, list):
                    if not all([isinstance(x, str) for x in val_here]):
                        raise MetaMergingError('Cannot merge string into a '
                                               'list containing other values'
                                               'than strings', _add_info)
                    self.__dict__[k].append(v)
                    continue
            raise MetaMergingError('Failed to merge', _add_info)
            
            
                

