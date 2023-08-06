"""
"""
import os

_path = os.path.dirname(__file__)
_vers_path = os.path.join(_path, "VERSION.txt")
with open(_vers_path) as inn:
    _version = inn.read().strip()

__version__ = _version
__author__ = "Luke Zoltan Kelley <lzkelley@northwestern.edu>"
__copyright__ = "Copyright 2019 - Luke Zoltan Kelley and contributors"
__contributors__ = []
__bibtex__ = """"""

_QUIET = True
_NUM_PAD = 1e-8

from kalepy import kernels   # noqa
from kalepy.kernels import *  # noqa
from kalepy import utils   # noqa
from kalepy.utils import *  # noqa

from kalepy.kde_base import KDE  # noqa

__all__ = []
__all__.extend(kernels.__all__)
__all__.extend(utils.__all__)
