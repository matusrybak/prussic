
import numpy as np
import math
import matplotlib as ml
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker
from matplotlib.ticker import MaxNLocator, MultipleLocator, AutoMinorLocator
from matplotlib import rc
from matplotlib.ticker import FormatStrFormatter
from scipy import stats

plt.rcParams["font.family"] = "sans"
plt.rcParams["mathtext.fontset"] = "stixsans"

Table  = open('HCN_ladders_Israel_2023.data')
I2023_ID, I2023_HCN_1010, I2023_HCN_2110, I2023_HCN_3210, I2023_HCN_4310, I2023_HCN_5410= np.genfromtxt(Table, unpack=True)
Table.close()

def UL(x, y, clr, EC, M = "o", size=50,Z = 2):
    plt.scatter([x], [y], facecolor=clr,  edgecolor = EC,s=size, marker=M,zorder=Z+3)
    plt.plot([x,x], [0.8*y, y], c = EC, lw=1 ,  zorder = Z+2)
    plt.scatter([x], [0.8*y], c = clr, edgecolor = EC, s=30, marker = 'v', zorder = Z+3)
    return()


def LL(x, y, clr, EC, M = "o", size=50,Z = 2):
    plt.scatter([x], [y], facecolor=clr,  edgecolor = EC,s=size, marker=M,zorder=Z+3)
    plt.plot([x,x], [y/0.8, y], c = EC, lw=1 ,  zorder = Z+2)
    plt.scatter([x], [y/0.8], c = clr, edgecolor = EC, s=30, marker = '^', zorder = Z+3)
    return()


fig = plt.figure()
ax=fig.add_subplot(111)
plt.ylabel(r"L'$_\mathrm{HCN(J-J-1)}$/L'$_\mathrm{HCN(1-0)}$", fontsize = 18)
plt.xlabel(r"J$_\mathrm{upp}$", fontsize = 18)

plt.tick_params(axis='both', which = 'major', length=10, direction = 'in', width=0.5, color = 'black', labelsize = 16)
plt.tick_params(axis='both', which = 'minor',length=5, direction = 'in', width=0.5, color = 'black', labelsize = 16)
#ax.xaxis.set_minor_locator(MultipleLocator(0.1))
#ax.yaxis.set_minor_locator(MultipleLocator(20))

plt.yscale('log')
plt.xlim(0.5, 4.5)
plt.ylim(5e-2, 2)


# z~0, from Israel+2023
# plot the median line
plt.plot([1,2,3,4], [1,0.41,0.33,0.19], c='0.33', lw=3, ls='dotted')
# plot the +/-1 sigma range (16th to 84th percentile)
plt.fill_between([1,2,3,4], [1,0.22,0.15,0.04],[1,0.64,0.51,0.34], fc='0.66',alpha=0.5)

# plot the same for the high-z galaxies
plt.plot([1,3,4], [1,0.59,0.41], c='darkorange', lw=3, ls='dotted')
plt.fill_between([1,3,4], [1,0.45,0.37],[1,0.76,0.45], fc='darkorange',alpha=0.5)

plt.text(3,0.8,"high-z",c='darkorange',fontsize=18)
plt.text(2,0.15,"z=0",c='0.5',fontsize=18)

#plt.legend(frameon=False, fontsize=12)
plt.gcf().set_size_inches(5,5)
#plt.savefig('fig_HCN_excitation.png', dpi = 100,
plt.savefig('fig_HCN_ladders_bands.png', dpi = 150, bbox_inches='tight')
