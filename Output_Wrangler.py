import numpy as np
import math as math
import pandas as pd
import matplotlib.pyplot as plt
import os
from astropy.io import fits

class BEAGLE_Wrangler:

    def __init__(self, beagle_output, samples):
        # File Wrangler (setting up parameters to extract data)
        os.chdir('/Users/alexander.steier/Python_Stockpile/BEAGLE_Outputs/'+beagle_output)
        count = 0
        while os.path.exists(str(count+1)+'_BEAGLE.fits'):
            count += 1
        
        # File properties
        galaxy_file_structure = fits.open(str(count)+'_BEAGLE.fits')
        number_of_galaxies = count
        number_of_bands = len(galaxy_file_structure[10].data[0])
        wavelength_range = galaxy_file_structure[8].data[0][0]
        number_of_params = len(galaxy_file_structure[12].data[0]) - 4 # .fits file structure
        sfh_time_length = len(galaxy_file_structure[6].data[0]['lookback_age'])
        og_photometry_data = fits.open('photo_data.fits')
        
        # Empty arrays to be filled
        file_names = np.empty(number_of_galaxies, dtype=np.dtype('U100'))
        galaxy_photometry = np.zeros((number_of_galaxies, samples, number_of_bands))
        sed_fits = np.zeros((number_of_galaxies, samples, len(wavelength_range)))
        params = np.zeros((number_of_galaxies, number_of_params, samples))
        sfh = np.zeros((number_of_galaxies, samples, sfh_time_length))
        sfh_time = np.zeros((number_of_galaxies, samples, sfh_time_length))
        og_photometry = np.zeros((number_of_galaxies, 2*number_of_bands))
        
        # Extracting data
        for i in range(number_of_galaxies):
            file_names[i] = str(i+1)+'_BEAGLE.fits'
            hdul = fits.open(file_names[i])
            
            for j in range(2*number_of_bands):
                og_photometry[i][j] = og_photometry_data[1].data[i][j+1]

            posterior_pdf = hdul[12].data[-samples-1:-1]
            for j in range(number_of_params):
                for k in range(samples):
                    params[i][j][k] = posterior_pdf[k][j+4]

            for k in range(samples):
                galaxy_photometry[i][k] = hdul[10].data[-1-samples+k]
                sed_fits[i][k] = hdul[9].data[-1-samples+k]
            
            sfh[i] = hdul[6].data['SFR'][-1-samples:-1]
            sfh_time[i] = hdul[6].data['lookback_age'][-1-samples:-1]

        param_names = []
        for j in range(number_of_params):
            param_names.append(hdul[12].header["TTYPE" + str(j+5)]) # 4 + 1

        #List of Attributes
        self.photometry = galaxy_photometry
        self.SEDs = sed_fits
        self.wavelength_range = wavelength_range
        self.params = params
        self.param_names = param_names
        self.sfh = sfh
        self.sfh_time = sfh_time
        self.number_of_galaxies = number_of_galaxies

    def spectra_plot(self):
        # Under Constuction
        plt.plot()
    
    def sfh_plot(self, galaxy_number):
        # Input Handler
        if galaxy_number == "all":
            galaxies = np.arange(self.number_of_galaxies)
        elif type(galaxy_number) == int:
            galaxies = np.array([galaxy_number-1])
        else:
            print("invalid galaxy number")
            galaxies = np.array([0])

        # Plotting
        for i in galaxies:
            x = self.sfh_time[i][0]
            y = self.sfh[i][0]
            plt.plot(x, y, label="Star Formation History")
            plt.xscale('log')
            plt.xlim((min(x), max(x)))
            plt.legend()
            plt.show()
            plt.close()
    
    def params_plot(self):
        # Under Construction
        plt.plot()


Fit20 = BEAGLE_Wrangler('Fit 20', 100)

Fit20.sfh_plot(1)