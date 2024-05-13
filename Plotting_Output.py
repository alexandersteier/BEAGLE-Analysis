from Output_Wrangler import BEAGLE_Wrangler
import numpy as np
import matplotlib.pyplot as plt
import os

fit_number = 25

Output = BEAGLE_Wrangler(f'Fit {fit_number}', 50)

number_of_params = len(Output.param_names)

for i in range(Output.number_of_galaxies):
    i += 1
    Output.params_plot(i)
    plt.subplot(4,4,1)
    plt.tick_params(axis='y', which='both', labelleft=False, left=False)
    plt.ylabel("")

    if number_of_params == 3:
        plt.subplot(3,3,2)
        Output.sfh_plot(i) # Replace with info box

        plt.subplot(3,3,3)
        Output.spectra_plot(i)

        plt.subplot(3,3,6)
        Output.sfh_plot(i)


    elif number_of_params == 4:
        plt.subplot(4,4,2)
        plt.xlim([0,1])
        plt.ylim([0,1])
        info = '\n'.join((r'%.0f samples' % (Output.samples),
                          Output.param_names[0] + r'$=%.3f\,\pm\,%.3f$' % (Output.params[i-1][0].mean(), Output.params[i-1][0].std()),
                          Output.param_names[1] + r'$=%.3f\,\pm\,%.3f$' % (Output.params[i-1][1].mean(), Output.params[i-1][1].std()),
                          Output.param_names[2] + r'$=%.3f\,\pm\,%.3f$' % (Output.params[i-1][2].mean(), Output.params[i-1][2].std()),
                          Output.param_names[3] + r'$=%.3f\,\pm\,%.3f$' % (Output.params[i-1][3].mean(), Output.params[i-1][3].std())
                         ))
        plt.text(0.05, 0.87, f"Parameters (Galaxy {i})", fontsize = 8, bbox = dict(edgecolor = 'white', facecolor = 'white', alpha = 1))
        plt.text(0.05, 0.47, info, fontsize = 5.3, bbox = dict(edgecolor = 'white', facecolor = 'white', alpha = 1))

        plt.subplot(2,2,2)
        Output.spectra_plot(i)
        plt.xlim(3e3, 5e4)
        plt.xticks([1e4, 2e4, 3e4, 4e4])
        plt.gca().set_xticks([0.5e4, 1.5e4, 2.5e4, 3.5e4, 4.5e4], minor=True)
        plt.tick_params(axis='y', which='both', labelleft=False, left=False, labelright=True, right=True, direction='in', pad=-32)
        plt.tick_params(axis='x', which='both', labelbottom=False, bottom=False, labeltop=True, top=True, direction='in', pad=-15)
        plt.xlabel(r"$\lambda_{\mathrm{obs}}$ ($\AA$)")
        plt.ylabel(r'$F_\nu$ (erg cm$^{-2}$ sec$^{-1}$ Hz$^{-1}$)', rotation=-90, labelpad=16)
        plt.gca().yaxis.set_label_position("right")
        plt.gca().xaxis.set_label_position("top")

        plt.subplot(4,4,12)
        Output.sfh_plot(i)
        axx = plt.gca().secondary_xaxis('top')
        axx.set_xticks([1e6, 1e8, 1e10])
        axx.tick_params(direction="in", which='both', pad=-15)
        axy = plt.gca().secondary_yaxis('right')
        axy.set_yticks([1e0, 1e2])
        axy.tick_params(direction="in", which='both', pad=-21)
        axy.tick_params(which='minor', right=False)
        axy.set_ylabel(r"SFR (M$_\odot$/yr)", rotation=-90, labelpad=16)

    elif number_of_params == 5:
        # May not work
        plt.subplot(5,5,3)
        Output.sfh_plot(i) # Replace with info box

        plt.subplot(3,3,3)
        Output.spectra_plot(i)

        plt.subplot(5,5,15)
        Output.sfh_plot(i)

    else:
        print("Not appropriate number of parameters")

    #"""
    folder = f'/Users/alexander.steier/Python_Stockpile/BEAGLE_Outputs/Fit{fit_number}_Correlation_Plots' 
    if not os.path.exists(folder):
        os.makedirs(folder)
    plt.savefig(f"/Users/alexander.steier/Python_Stockpile/BEAGLE_Outputs/Fit{fit_number}_Correlation_Plots/Fit{fit_number}_Correlation{i}.png", 
                transparent=None, dpi=160, format='png', pad_inches=0.1)
    #"""

    #plt.show()
    plt.close()