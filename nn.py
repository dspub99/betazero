#!/usr/bin/env python

from collections import OrderedDict
import sys, copy
import numpy as np

class NN:
    def __init__(self, ww):
        if type(ww)==type(OrderedDict()):
            self._ww = ww['weights']
        else:
            self._ww = ww
        
    def __call__(self, x):
        a = x
        for w in self._ww:
             a = np.tanh(w[0,:] + a.dot(w[1:,:]))
        return a

    def sDict(self):
        return {'weights': self._ww}

class NNFactory:
    def __init__(self, nx, na, nhs):
        # nhs = [nh1, nh2, nh3, ...]
        self.nx = nx
        self.na = na
        self.nhs = copy.copy(nhs)
        self.nhs.append(self.na)
        np = 0
        nprev = self.nx
        for nh in self.nhs:
            np += nh*(1+nprev)
            nprev = nh
        self.nParams = np

    def numParams(self):
        return self.nParams

    def __call__(self, w):
        ww = []
        i0=0
        nprev = self.nx
        for nh in self.nhs:
            n = nh*(1+nprev)
            ww.append( np.reshape(w[i0:i0+n],(1+nprev, nh)) )
            nprev = nh
            i0 += n
        assert(i0 == w.size)

        return NN(ww)




