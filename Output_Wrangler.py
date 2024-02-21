import numpy as np
import math as math
import pandas as pd
import matplotlib.pyplot as plt
import os
from astropy.io import fits
from scipy import constants

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
        ref_photometry_data = fits.open('photo_data.fits')
        filters = fits.open('filter_catalog.fits')
        
        # Empty arrays to be filled
        file_names = np.empty(number_of_galaxies, dtype=np.dtype('U100'))
        galaxy_photometry = np.zeros((number_of_galaxies, samples, number_of_bands))
        sed_fits = np.zeros((number_of_galaxies, samples, len(wavelength_range)))
        params = np.zeros((number_of_galaxies, number_of_params, samples))
        sfh = np.zeros((number_of_galaxies, samples, sfh_time_length))
        sfh_time = np.zeros((number_of_galaxies, samples, sfh_time_length))
        og_photometry = np.zeros((number_of_galaxies, 2*number_of_bands))
        wavelength_range_obs = np.zeros((number_of_galaxies, samples, len(wavelength_range)))
        redshift = np.zeros((number_of_galaxies, samples, len(wavelength_range)))
        
        # Extracting data
        for i in range(number_of_galaxies):
            file_names[i] = str(i+1)+'_BEAGLE.fits'
            hdul = fits.open(file_names[i])
            
            for j in range(2*number_of_bands):
                og_photometry[i][j] = ref_photometry_data[1].data[i][j+1]

            posterior_pdf = hdul[12].data[-samples-1:-1]
            for j in range(number_of_params):
                for k in range(samples):
                    params[i][j][k] = posterior_pdf[k][j+4]

            for k in range(samples):
                galaxy_photometry[i][k] = hdul[10].data[-1-samples+k]
                sed_fits[i][k] = hdul[9].data[-1-samples+k]
                redshift[i][k] = np.full(len(wavelength_range), hdul[1].data[-1-samples+k][0])
                wavelength_range_obs[i][k] = wavelength_range * (1 + redshift[i][k][0])
            
            sfh[i] = hdul[6].data['SFR'][-1-samples:-1]
            sfh_time[i] = hdul[6].data['lookback_age'][-1-samples:-1]

        param_names = []
        for j in range(number_of_params):
            param_names.append(hdul[12].header["TTYPE" + str(j+5)]) # 4 + 1

        filter_width = np.zeros(number_of_bands)
        filter_center = np.zeros(number_of_bands)
        for j in range(number_of_bands):
            band = filters[1].data[0][j]
            filter_wavelength_range = band[0][band[1] > 0.5 * max(band[1])]
            filter_width[j] = filter_wavelength_range[-1] - filter_wavelength_range[0]
            filter_center[j] = np.median(filter_wavelength_range)

        #List of Attributes
        self.number_of_galaxies = number_of_galaxies
        self.samples = samples
        self.number_of_bands = number_of_bands
        self.redshift = redshift
        self.photometry = galaxy_photometry
        self.SEDs = sed_fits
        self.wavelength_range_rest = wavelength_range
        self.wavelength_range_obs = wavelength_range_obs
        self.params = params
        self.param_names = param_names
        self.sfh = sfh
        self.sfh_time = sfh_time
        self.reference_data = 1e-23 * og_photometry
        self.filter_center = filter_center
        self.filter_width = filter_width

    def spectra_plot(self, galaxy_number, suppress=True):
         # Input Handler
        if galaxy_number == "all":
            galaxies = np.arange(self.number_of_galaxies)
        elif type(galaxy_number) == int:
            galaxies = np.array([galaxy_number-1])
        else:
            print("invalid galaxy number")
            galaxies = np.array([0])

        # Physics 
        Flux = 10 ** (- (self.photometry + 48.60) / 2.5) # Conversion from mag to flux density
        SEDs = self.SEDs * (self.wavelength_range_obs)**2 / ((1+self.redshift) * (constants.c*10**10))


        # Reference Data Handler
        reference_photometry = np.zeros((self.number_of_galaxies, self.number_of_bands))
        reference_photometry_error = np.zeros((self.number_of_galaxies, self.number_of_bands))
        for i in range(self.number_of_galaxies):
            for j in range(self.number_of_bands):
                reference_photometry[i][j] = self.reference_data[i][2*j]
                reference_photometry_error[i][j] = self.reference_data[i][2*j+1]

        # Plotting
        for i in galaxies:
            for k in range(self.samples):
                plt.plot(self.wavelength_range_obs[i][k], SEDs[i][k], color='slategrey', alpha=1/self.samples)
                plt.errorbar(self.filter_center, Flux[i][k], color='tab:orange', marker='.', linestyle='none', alpha=0.1)
            plt.errorbar(self.filter_center, reference_photometry[i], reference_photometry_error[i], 0.5*self.filter_width, marker='.', linestyle='none')
            
            # Designing legend
            plt.errorbar(-1,-1,1,1, color='tab:blue', marker='.', label='Yuma+17 Photometry')
            plt.scatter(-1,-1, color='tab:orange', marker='.', label='BEAGLE Photometry')
            plt.plot(-1, -1, color='slategrey', label='BEAGLE SED Fit')
            plt.legend(loc=4)

            # Plot Customization
            plt.yscale('log')
            plt.xlim((0, 5e4))
            plt.ylim((0.5*reference_photometry[i].min(), 10*reference_photometry[i].max()))
            plt.xlabel(r'Wavelength (${\AA}$)', fontsize='large')
            plt.ylabel(r'$F_\nu$ (erg cm$^{-2}$ sec$^{-1}$ Hz$^{-1}$)', fontsize='large')
            plt.title('Spectral Energy Distribution (Galaxy ' + str(i+1) + ')', fontsize='large')
            if suppress == False:
                plt.show()
                plt.close()
    
    def sfh_plot(self, galaxy_number, suppress=True):
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
            for k in range(self.samples):
                plt.plot(self.sfh_time[i][k], self.sfh[i][k], alpha=1/self.samples, color='tab:green')
            plt.plot(-1, -1, label="Star Formation History", color='tab:green')
            plt.xlim((1e4, 1e10))
            plt.xscale('log')
            plt.xlabel("Lookback Time (yr)")
            plt.ylabel(r"SFR (M$_\odot$/yr)")
            plt.legend()
            if suppress == False:
                plt.show()
                plt.close()
    
    def params_plot(self, galaxy_number, suppress=True):
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
            df = pd.DataFrame(self.params[i].transpose(), columns=self.param_names)
            pd.plotting.scatter_matrix(df, figsize=(8,8), marker = '.', hist_kwds = {'bins': 11, 'color': "tab:purple"}, alpha = 0.85, range_padding=0.2, color="tab:purple")
            if suppress == False:
                plt.show()
                plt.close()