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

    def __init__(self, beagle_output, samples):
        # File Wrangler (setting up parameters to extract data)
        os.chdir('/Users/alexander.steier/Python_Stockpile/BEAGLE_Outputs/'+beagle_output)
        try:
            count = 0
            while True:
                count += 1
                hdul = fits.open(str(count+1)+'_BEAGLE.fits')
        except:
              number_of_galaxies = count

        number_of_bands = len(hdul[10].data[0])
        wavelength_range = hdul[8].data[0][0]
        
        file_names = np.empty(number_of_galaxies, dtype=np.dtype('U100'))
        galaxy_photometry = np.zeros((number_of_galaxies, samples, number_of_bands))
        sed_fits = np.zeros((number_of_galaxies, samples, len(wavelength_range)))
        
        # Extracting data
        for i in range(number_of_galaxies):
            file_names[i] = str(i+1)+'_BEAGLE.fits'
            hdul = fits.open(file_names[i])
            for j in range(samples):
                galaxy_photometry[i][j] = hdul[10].data[-j-1]
                sed_fits[i][j] = hdul[9].data[-j-1]
            gprop = hdul[12].data
        print(galaxy_photometry)
        print(sed_fits)

        #List of Attributes
        self.photometry = galaxy_photometry
        self.SEDs = sed_fits
        self.wavelength_range = wavelength_range
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


Fit20 = BEAGLE_Wrangler('Fit 20', 100)

plt.plot(Fit20.wavelength_range, Fit20.SEDs[0][99])
plt.show()