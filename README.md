# BEAGLE-Analysis
This repository is designed to allow for data analysis of BEAGLE outputs.
BEAGLE is an SED fitting code that accounts for spectral emission lines along with stellar emission.
Output_Wrangler.py is designed to convert the .fits file outputs into well structured numpy arrays, and plot this data
Plotting_Output.py produces a figure with a covariance plot, an SED, and the SFH.
Plot.py is a space to plot whatever is needed.

The input this program takes is the unzipped .fits file output of BEAGLE, as well as the input .fits files for the filter curves and the photometry data.

Note that the program takes a while to run for a large set of galaxies, even if only plotting a single galaxy. Initializing the class reads in all data.

Additional Features to be added.