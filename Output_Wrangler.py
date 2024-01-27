import numpy as np
import math as math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import scipy
from scipy import constants
from scipy.stats import chi2
from scipy.optimize import curve_fit
import os
from astropy.io import fits

class BEAGLE_Wrangler:

    def __init__(self, beagle_output):
        #Incomlete list
        self.numpy = beagle_output

    def spectra(self):
        # Under Constuction
        spectra = self.numpy
        return spectra
    
    def sfh(self):
        # Under Construction
        sfh = self.numpy
        return sfh
    
    def params(self):
        # Under Construction
        params = self.numpy
        return params
