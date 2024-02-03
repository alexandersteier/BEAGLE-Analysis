from Output_Wrangler import BEAGLE_Wrangler

Output = BEAGLE_Wrangler('Fit 20', 100)

#Output.spectra_plot(20)
#Output.sfh_plot(20)
Output.params_plot("all")