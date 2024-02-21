from Output_Wrangler import BEAGLE_Wrangler
import matplotlib.pyplot as plt

Output = BEAGLE_Wrangler('Fit 20', 100)

Output.params_plot(42)

plt.subplot(442)
Output.sfh_plot(42)

plt.subplot(222)
Output.spectra_plot(42)

plt.show()
plt.close()