from Output_Wrangler import BEAGLE_Wrangler
import numpy as np
import matplotlib.pyplot as plt

Output = BEAGLE_Wrangler('Fit 20', 100)

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
        plt.title(f"Parameters (Galaxy {i})", size="small")
        plt.xlim([0,1])
        plt.ylim([0,1])
        info = '\n'.join((r'%.0f samples' % (Output.samples),
                          Output.param_names[0] + r'$=%.3f\,\pm\,%.3f$' % (Output.params[i][0].mean(), Output.params[i][0].std()),
                          Output.param_names[1] + r'$=%.3f\,\pm\,%.3f$' % (Output.params[i][1].mean(), Output.params[i][1].std()),
                          Output.param_names[2] + r'$=%.3f\,\pm\,%.3f$' % (Output.params[i][2].mean(), Output.params[i][2].std()),
                          Output.param_names[3] + r'$=%.3f\,\pm\,%.3f$' % (Output.params[i][3].mean(), Output.params[i][3].std())
                         ))
        plt.text(0.05, 0.67, info, fontsize = 5.3, bbox = dict(edgecolor = 'white', facecolor = 'white', alpha = 1))

        plt.subplot(2,2,2)
        Output.spectra_plot(i)
        plt.tick_params(axis='y', which='both', labelleft=False, left=False, labelright=True, right=True)
        plt.tick_params(axis='x', which='both', labelbottom=False, bottom=False, labeltop=True, top=True)

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

    plt.show()
    plt.close()