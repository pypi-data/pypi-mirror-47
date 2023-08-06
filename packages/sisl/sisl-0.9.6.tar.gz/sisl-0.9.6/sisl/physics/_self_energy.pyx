#!python
#cython: language_level=2
cimport cython
from libc.math cimport fabs

import numpy as np
cimport numpy as np
cimport scipy.linalg.cython_blas as B
cimport scipy.linalg.cython_lapack as L


__all__ = ['lsls_se', 'lsls_se_lr', 'lsls_se_bulk']


def lsls_se(H00, H01, E, S00, S01):
