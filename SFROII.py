import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import os
from Output_Wrangler import BEAGLE_Wrangler

old_set = np.array([1,5,7,15,18,24,30,32]) - 1
recent_set = np.array([2,8,9,16,19,20,42]) - 1
burst_set = np.array([17,21,25,33,35,40]) - 1
prolonged_set = np.array([4,6,10,12,13,14,22,23,26,27,28,29,31,34,36,37,38,39,41]) - 1
unfit_set = np.array([3, 11]) - 1 # 3 has no good fit, 11 is a duplicate


model_number = 23
alt_model_number = 25

Output = BEAGLE_Wrangler(f'Fit {model_number}', 50)
altOutput = BEAGLE_Wrangler(f'Fit {alt_model_number}', 50)

LOII = np.array([[22.6, 2.7], [19.9, 2.7], [18.5, 2.7], [23.8, 4.0], [14.9, 2.7], [15.1, 2.7], [9.45, 1.3], [14.1, 2.7], [11.3, 2.7], [13.5, 2.7], [13.5, 2.7], [23.6, 4.0], [19.9, 4.0], [10.8, 2.7], [11.8, 2.7], [19.2, 4.0], [32.7, 5.3], [18.3, 4.0], [29.2, 5.3], [10.7, 2.7], [16.3, 4.0], [22.5, 4.0], [20.7, 4.0], [11.3, 2.7], [17.8, 4.0], [20.5, 4.0], [23.4, 5.3], [6.70, 1.3], [18.6, 4.0], [8.54, 1.3], [17.0, 4.0], [9.84, 2.7], [21.4, 5.3], [18.1, 4.0], [9.85, 2.7], [9.71, 2.7], [13.1, 2.7], [9.30, 2.7], [10.5, 2.7], [14.7, 4.0], [8.17, 2.7], [18.4, 5.3]])
B = np.array([[25.2502, 0.0135], [24.3641, 0.0063], [26.1266, 0.0304], [23.2010, 0.0019], [25.5558, 0.0287], [23.7089, 0.0033], [26.5405, 0.0429], [24.1273, 0.0051], [25.8920, 0.0201], [24.1882, 0.0046], [24.1882, 0.0046], [23.3654, 0.0027], [23.1407, 0.0022], [24.2486, 0.0042], [24.4437, 0.0079], [24.5750, 0.0084], [23.1042, 0.0020], [26.1573, 0.0254], [23.4228, 0.0025], [24.8844, 0.0071], [24.1145, 0.0039], [23.1524, 0.0022], [23.2482, 0.0020], [25.8846, 0.0197], [23.2529, 0.0021], [23.3952, 0.0022], [23.3084, 0.0025], [24.3609, 0.0062], [24.1251, 0.0041], [25.7511, 0.0168], [23.2251, 0.0021], [25.3923, 0.0146], [23.5706, 0.0020], [23.7707, 0.0031], [24.4838, 0.0061], [24.2344, 0.0045], [23.5832, 0.0028], [24.0487, 0.0040], [24.7187, 0.0062], [23.4829, 0.0022], [24.6423, 0.0058], [24.4345, 0.0061]])
BMAG = B[:,0]
BMAGerr = [B[:,0] + B[:,1], B[:,0] - B[:,1]]

def fB(m):
    M = m - 5 * (np.log10(10550.3 * 1e6) - 1) # Mag conversion
    # return 0.032 * (M + 16.4)**2 + 0.03 # Moustakas 2006
    return 0.013 * (M + 16.4)**2 + 0.03 # adjusted

SFROII = LOII[:,0] * 10 ** fB(BMAG)
SFROIIerr = 3e2*(LOII[:,1] * 10 ** fB(BMAGerr[1]) - LOII[:,1] * 10 ** fB(BMAGerr[0]))
# SFROIIerr = 10*(LOII[:,1] * 10 ** fB(BMAGerr[1]) - LOII[:,1] * 10 ** fB(BMAGerr[0])) # Moustakas 2006

SFRSIM = 10**Output.params.mean(axis=2)[:,1]
SFRSIMerr = 10**Output.params.max(axis=2)[:,1] - 10**Output.params.min(axis=2)[:,1]
#SFRSIM[burst_set] = 10**altOutput.params.mean(axis=2)[:,2][burst_set] #introduces alternate set

Mass = 10**Output.params.mean(axis=2)[:,0]
sSFR = SFRSIM/Mass
ssfr = np.log10(sSFR)

norm = matplotlib.colors.Normalize(vmin=min(ssfr), vmax=max(ssfr), clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap='viridis')
sSFR_color = np.array([(mapper.to_rgba(v)) for v in ssfr])
plot = plt.scatter(-SFROII, ssfr, s=0, c=ssfr)
clb = plt.colorbar(plot, label="log(sSFR) (yr$^{-1}$)")
plot = plt.plot(np.arange(200), np.arange(200), color='black')

count = 0
for x, y, xerr, yerr, color in zip(SFROII, SFRSIM, SFROIIerr, SFRSIMerr, sSFR_color):
    if np.isin(count, old_set):
        plt.plot(x, y, 'v', color=color)
        plt.errorbar(x, y, yerr, xerr, lw=1, capsize=2, color=color, linestyle="none")
    if np.isin(count, recent_set):
        plt.plot(x, y, '^', color=color)
        plt.errorbar(x, y, yerr, xerr, lw=1, capsize=2, color=color, linestyle="none")
    if np.isin(count, prolonged_set):
        plt.plot(x, y, '.', color=color)
        plt.errorbar(x, y, yerr, xerr, lw=1, capsize=2, color=color, linestyle="none")
    if np.isin(count, burst_set):
        plt.plot(x, y, '*', color=color)
        plt.errorbar(x, y, yerr, xerr, lw=1, capsize=2, color=color, linestyle="none")
    count += 1

plt.errorbar(-1, -1, 0, 0, linestyle="none", marker='*', label="burst", color='black')
plt.errorbar(-1, -1, 0, 0, linestyle="none", marker='v', label="old", color='black')
plt.errorbar(-1, -1, 0, 0, linestyle="none", marker='.', label="prolonged", color='black')
plt.errorbar(-1, -1, 0, 0, linestyle="none", marker='^', label="recent", color='black')

plt.ylabel("BEAGLE SFR (M$_\odot$/yr)")
plt.xlabel(r"SFR from L[OII] (M$_\odot$/yr)")
plt.xlim(0,110)
plt.ylim(0,110)
plt.legend()
plt.show()

"""
folder = f'/Users/alexander.steier/Python_Stockpile/BEAGLE_Outputs/Fit{model_number}_Plots' 
if not os.path.exists(folder):
    os.makedirs(folder)
plt.savefig(f"/Users/alexander.steier/Python_Stockpile/BEAGLE_Outputs/Fit{model_number}_Plots/SFR.png", 
        transparent=None, dpi=160, format='png', pad_inches=0.1)
"""