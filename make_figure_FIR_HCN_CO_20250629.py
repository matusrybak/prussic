
import numpy as np
import math
import matplotlib as ml
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker
from matplotlib.ticker import MaxNLocator, MultipleLocator, AutoMinorLocator
from matplotlib import rc
from matplotlib.ticker import FormatStrFormatter

plt.rcParams["font.family"] = "sans"
plt.rcParams["mathtext.fontset"] = "stixsans"

Table  = open('table_VLA_targets.data')
VLA_FIR, VLA_LCO, VLA_mu, VLA_HCN = np.genfromtxt(Table, unpack=True, usecols = (2,3,4,5))
Table.close()


def read_table_as_dict(filename):
    with open(filename) as f:
        lines = [line for line in f if line.strip() and not line.lstrip().startswith('#')]

    headers = [h.strip() for h in lines[0].split(',')]
    table = {h: [] for h in headers}

    for line in lines[1:]:
        values = line.strip().split(',')
        for h, v in zip(headers, values):
            v = v.strip()
            if not v or v.lower() == 'nan':
                value = np.nan
            else:
                try:
                    value = float(v)
                except ValueError:
                    value = v
            table[h].append(value)

    return table


table_dict = read_table_as_dict('../MasterTableLines_20250717.csv')
print (table_dict.keys())
SMG_HCN = np.asarray(table_dict['HCN(4-3)'])
SMG_HCN_err = np.asarray(table_dict['Delta_HCN(4-3)'])



SMG_FIR =  np.asarray(table_dict['LFIR_sky'])
SMG_FIR_rms =  np.asarray(table_dict['LFIR_sky_sigma'])

SMG_LCO = np.asarray(table_dict["LCO"])
SMG_LCO_err = np.asarray(table_dict["LCO_sigma"])

SMG_mu =  np.asarray(table_dict['mu'])
SMG_Name = table_dict["Source_ID"]




Table  = open('table_Rybak2021_SMGs.data')
R21_FIR, R21_LCO, R21_mu, R21_HCN, R21_HCN_err = np.genfromtxt(Table, unpack=True, usecols = (2,3,4,5,6))
Table.close()
R21_Name = ['SDP.81','SDP.130','HXMM.02','9io9', 'J1202', 'J1609']
R21_HCN*=1./0.76


Table  = open('table_Gao2004.data')
GS2004_LFIR, GS2004_HCN_CO, GS2004_FIR_HCN = np.genfromtxt(Table, unpack=True, usecols = (2,5,6))
Table.close()

GS2004_LFIR*=1.e10

Table  = open('table_ULIRGS_GB2012.data')
GB2012_LFIR, GB2012_HCN_FIR, GB2012_HCN_CO = np.genfromtxt(Table, unpack=True)
Table.close()

fig = plt.figure()
ax=fig.add_subplot(111)
#plt.xlabel(r'L$_\mathrm{FIR}$ [$L_\odot$] $\propto$ SFR', fontsize = 12)
plt.xlabel(r'Star-formation rate [$M_\odot$/yr]', fontsize = 13)
#plt.ylabel(r"L'$_\mathrm{HCN(1-0)}$/L$_\mathrm{FIR}$ ", fontsize = 10)
plt.ylabel(r"HCN/CO $\propto$ dense-gas fraction ", fontsize = 13)

#plt.locator_params(nbins=5)
plt.tick_params(axis='both', which = 'major', length=10, direction = 'in', width=0.5, color = 'black', labelsize = 10)
plt.tick_params(axis='both', which = 'minor',length=5, direction = 'in', width=0.5, color = 'black', labelsize = 10)
ax.xaxis.set_minor_locator(MultipleLocator(0.01))
#ax.yaxis.set_minor_locator(MultipleLocator(20))


plt.xscale('log')
#plt.xlim(1e10, 1e14)
plt.xlim(0.1, 1e4)
plt.yscale('log')
plt.ylim(0.01, 1)
#plt.yticks([0,0.1,0.2,0.3,0.4])
def UL(x, y, clr, size=30):
    plt.scatter([x], [y], facecolor=clr, edgecolor = clr, s=size)
    plt.plot([x, x], [0.8*y,y], c = clr, lw=2 )
    plt.scatter([x], [0.8*y], c = clr, edgecolor = clr,s=30, marker = 'v')
    return()

#EMPIRE
plt.fill_between([1.71e-10*1.e8, 1.71e-10*1.e10],[0.0206, 0.0206],[0.0293,0.0293], color = '0.5', alpha=0.33)
plt.text(0.35, 0.025, "EMPIRE",fontsize = 14, va = 'center', ha='center', color = '0')



#for i in range(6):
#    if R21_HCN[i]<0.0:
#        UL(R21_FIR[i]/R21_mu[i]*1.71e-10, -R21_HCN[i]/R21_LCO[i],'dodgerblue',100)

#    else:
#        plt.scatter(R21_FIR[i]/R21_mu[i]*1.71e-10,R21_HCN[i]/R21_LCO[i], color='dodgerblue',s = 100, label = 'high-redshift, Rybak+2022')

#plt.text(R21_FIR[6]*1.71e-10,0.042*1.2,'Stack, Rybak+22', color = 'darkorange', horizontalalignment = 'center')
UL(R21_FIR[6]*1.71e-10,0.042, 'darkorange', 150)


# SDP.9
plt.scatter([1.4e13*1.71e-10],[0.29], c='0', s=25, label = 'high-redshift, archival')

UL(1.1e13,0.19*1.71e-10, '0')

# Gao & Solomon - de-lensed?
plt.scatter( [0.93e12*1.71e-10],[0.15], c='0', s=25, zorder = 5)

UL(22e12*1.71e-10,28./159., '0')
UL(6.1e12*1.71e-10,3.7/19., '0')
UL(2.1e12*1.71e-10, 0.6/4.8,'0')

#plt.scatter(GS2004_LFIR*1.71e-10,GS2004_HCN_CO,s=50, c = '0.75', edgecolor = '0',lw=0.5, label = 'nearby galaxies', zorder = 1)
plt.scatter(GS2004_LFIR*1.71e-10,GS2004_HCN_CO,s=50, c = '0.5', marker = 'x',lw=1.5, label = 'nearby galaxies', zorder = 1)
plt.scatter(GB2012_LFIR*1.71e-10,GB2012_HCN_CO,s=50, c = '0.5', marker = 'x', lw=1.5,zorder = 1)



r_41 = 0.41
SMG_HCN/=r_41
for i in range(len(SMG_HCN)):
    if SMG_HCN[i]<0.0:
        UL(SMG_FIR[i]/SMG_mu[i]*1.71e-10, -SMG_HCN[i]/SMG_LCO[i],'royalblue',100)
    else:
        plt.scatter(SMG_FIR[i]/SMG_mu[i]*1.71e-10,SMG_HCN[i]/SMG_LCO[i], color='royalblue',s = 100)
        plt.errorbar(SMG_FIR[i]/SMG_mu[i]*1.71e-10,SMG_HCN[i]/SMG_LCO[i], yerr = SMG_HCN[i]/SMG_LCO[i]*np.sqrt(SMG_HCN_err[i]**2/SMG_HCN[i]**2+SMG_LCO_err[i]**2/SMG_LCO[i]**2),color='royalblue')


#plt.fill_between([0.1,1e4],[0.01,0.01],[0.1,0.1], fc='cornflowerblue', alpha=0.2, zorder=0)
#plt.fill_between([0.1,1e4],[0.1,0.1],[1,1], fc='salmon', alpha=0.2, zorder=0)

#plt.text(0.15,0.7, "dense-gas rich", c='salmon',fontsize=16,zorder=10)
#plt.text(0.15,0.07, "dense-gas poor", c='royalblue',fontsize=16,zorder=10)

plt.gcf().set_size_inches(6,5)
#plt.legend(scatterpoints = 1, loc = 'lower right')

plt.savefig('fig_FIR_HCN_over_CO_2025.png', dpi = 200, bbox_inches='tight')
