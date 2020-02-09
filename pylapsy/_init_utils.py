# -*- coding: utf-8 -*-
import logging
from os.path import abspath, dirname
from pkg_resources import get_distribution

def _init_supplemental():
    return (get_distribution('pylapsy').version, abspath(dirname(__file__)))

def _init_logger():
    ### LOGGING
    # Note: configuration will be propagated to all child modules of
    # pylapsy, for details see
    # http://eric.themoritzfamily.com/learning-python-logging.html
    logger = logging.getLogger('pylapsy')

    fmt = "%(filename)s(l%(lineno)s,%(funcName)s()): %(message)s"
    #fmt = "%(funcName)s():%(lineno)i: %(message)s"
    default_formatter = logging.Formatter(fmt)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(default_formatter)

    logger.addHandler(console_handler)

    logger.setLevel(logging.WARNING)

    print_log = logging.getLogger('pylapsy_print')

    print_handler = logging.StreamHandler()
    print_handler.setFormatter(logging.Formatter("%(message)s"))

    print_log.addHandler(print_handler)

    print_log.setLevel(logging.INFO)
    return (logger, print_log)

def _get_loglevels():
    
    return dict(critical=logging.CRITICAL,
                exception=logging.ERROR,
                error=logging.ERROR,
                warn=logging.WARNING,
                warning=logging.WARNING,
                info=logging.INFO,
                debug=logging.DEBUG)

def get_loglevel(logger):
    return logger.getEffectiveLevel()

def change_loglevel(logger, level, update_fmt=False, fmt_debug=True):
    LOG_LEVELS = _get_loglevels()
    if level in LOG_LEVELS:
        logger.setLevel(LOG_LEVELS[level])
    else:
        try:
            logger.setLevel(level)
        except Exception as e:
            raise ValueError('Could not update loglevel, invalid input. Error: {}'.format(repr(e)))
    if update_fmt:
        import logging
        if fmt_debug:
            fmt = logging.Formatter("%(filename)s(l%(lineno)s,%(funcName)s()): %(message)s")
        else:
            fmt = logging.Formatter("%(message)s")
        for handler in logger.handlers:
            handler.setFormatter(fmt)

def _check_requirements():
    try:
        import cv2
        CV2AVAILABLE = True
    except BaseException:
        CV2AVAILABLE = False
    return (CV2AVAILABLE)

def init_add_data():
    import os
    from .io import data_dir
    BASEDIR_DATA = data_dir()
    DATADIR_DESHAKE_TEST = os.path.join(BASEDIR_DATA, 'test_data', 'deshake')
    return (BASEDIR_DATA, DATADIR_DESHAKE_TEST)