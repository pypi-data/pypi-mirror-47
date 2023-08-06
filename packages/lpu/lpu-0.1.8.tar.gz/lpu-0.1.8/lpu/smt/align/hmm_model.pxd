# 3-rd party library
cimport numpy as np
from numpy cimport ndarray

# local
from . ibm_model1 cimport Model1
from . ibm_model1 cimport Model1Trainer

cdef class ModelHMM(Model1):
    pass

cdef class HMMTrainer(Model1Trainer):
    pass

