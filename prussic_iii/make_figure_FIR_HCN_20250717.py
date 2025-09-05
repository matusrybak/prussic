
import numpy as np
import math
import matplotlib as ml
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker
from matplotlib.ticker import MaxNLocator, MultipleLocator, AutoMinorLocator
from matplotlib import rc
from matplotlib.ticker import FormatStrFormatter
import csv

plt.rcParams["font.family"] = "sans"
plt.rcParams["mathtext.fontset"] = "stixsans"

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

SMG_CO = np.asarray(table_dict["LCO"])
SMG_CO_rms = np.asarray(table_dict["LCO_sigma"])

SMG_mu =  np.asarray(table_dict['mu'])
SMG_Name = table_dict["Source_ID"]



Table  = open('table_Rybak2021_SMGs.data')
R21_FIR, R21_LCO, R21_mu, R21_HCN, R21_HCN_err = np.genfromtxt(Table, unpack=True, usecols = (2,3,4,5,6))
Table.close()
R21_Name = ['SDP.81','SDP.130','HXMM.02','9io9', 'J1202', 'J1609']

for i in range(6):
    print (R21_Name[i], R21_HCN[i]/R21_FIR[i])

#Table  = open('../Compare_FIR_HCN_HCO+/table_SMGs.data')
#SMG_Ref, SMG_Z, SMG_FIR, SMG_mu, SMG_HCN, SMG_HCN_err, SMG_HCO, SMG_HCO_err = np.genfromtxt(Table, unpack=True, usecols=(1,2,3,5,6,7,8,9))
#Table.close()



Table  = open('table_ULIRGS_GB2012.data')
GB2012_LFIR, GB2012_HCN_FIR, GB2012_HCN_CO = np.genfromtxt(Table, unpack=True)
Table.close()

fig = plt.figure()
ax=fig.add_subplot(111)
plt.xlabel(r'Star-formation rate [M$_\odot$/yr]', fontsize = 13)
#plt.ylabel(r"L'$_\mathrm{HCN(1-0)}/$L$_\mathrm{FIR}$ $\propto$ 1/SFE", fontsize = 13)
plt.ylabel(r"HCN(1-0)/FIR $\propto$ 1/SFE", fontsize = 13)

#plt.locator_params(nbins=5)
plt.tick_params(axis='both', which = 'major', length=10, direction = 'in', width=0.5, color = 'black', labelsize = 10)
plt.tick_params(axis='both', which = 'minor',length=5, direction = 'in', width=0.5, color = 'black', labelsize = 10)
#ax.xaxis.set_minor_locator(MultipleLocator(0.1))
#ax.yaxis.set_minor_locator(MultipleLocator(20))

plt.xscale('log')
plt.yscale('log')

plt.xlim(0.1, 1e4)
plt.ylim(1e-4,1e-2)

def UL(x, y, clr, size=50):
    plt.scatter([x], [y], facecolor=clr,  edgecolor = clr,s=size, zorder=5)
    plt.plot([x,x], [0.85*y, y], c = clr, lw=1 , zorder = 2)
    plt.scatter([x], [0.85*y], c = clr, edgecolor = clr, s=30, marker = 'v', zorder = 5)
    return()


# Gao & Solomon 2004
Gao2004_LFIR = np.asarray([2.1,46.7,3.7,46.6,25.7,2.6,2.6,2.1,28.3,25.1,12.9,1.4,38.6,87.1, 118.1,10., 6.2,45.7,0.83,89.2,4.6,4.3,93.8,36.5,1.35])*1e10
Gao2004_LHCN = np.asarray([0.27, 8.5, np.nan, 4.3,1.89,0.25,0.20,np.nan,3.61,2.67,3.10,0.47,1.25,9.8,6.2,0.96,0.40,3.8,np.nan,10.,0.3,1.0,10.2,4.0,np.nan])*1.e8
plt.scatter(Gao2004_LFIR*1.71e-10,Gao2004_LHCN/Gao2004_LFIR, s=50, c = '0.5',marker='x',edgecolor = 'none', label = 'z=0')



# Garcia-Burillo+2012
plt.scatter(GB2012_LFIR*1.71e-10,GB2012_HCN_FIR, s=50, c = '0.5',marker='x', edgecolor = '0')

# Krips+2008, source: Jimenez-Donaire+2019
Krips_LFIR = np.array((10.8136,9.49601,9.14275,9.22923,9.58508,9.45516,10.6883,10.1939,11.9754))
Krips_LHCN = np.array((8.15425,6.95629,6.442,6.51264,7.21742,6.79601,7.38231,6.845,9.05306))
plt.scatter(10.**Krips_LFIR*1.71e-10,10.**Krips_LHCN/10.**Krips_LFIR, s=50, c = '0.5',marker='x',edgecolor = 'none')


#EMPIRE
plt.fill_between([1.e8*1.71e-10, 1.e10*1.71e-10],[1./977.*10**0.37, 1./977.*10**0.37],[1./977./10**0.37, 1./977./10**0.37], color = '0.5', alpha=0.33)
plt.text(10**9.3*1.71e-10, 1/977, "EMPIRE", verticalalignment = 'center', fontsize = 14, horizontalalignment='center', color = '0.25')
#Gerben's thesis
#plt.text(1.9e13,1.87e10/1.9e13*1.1,'GN20', color = 'teal', horizontalalignment = 'center')
#UL(1.9e13, 1.87e10/1.9e13, 'teal',100)


# Eyelash
UL(2.3e12*1.71e-10, 4.5e9/2.3e12, '0')

# Gao+2007 - de-lensed
plt.text(0.93e12*1.71e-10,0.6e9/0.93e12*1.1,'J16359', color = '0', horizontalalignment = 'center')
plt.scatter([0.93e12*1.71e-10],[0.6e9/0.93e12],  c='0', s=50)
UL(6.1e12*1.71e-10, 3.7/6.1e3,'0')    #J02396-0134
UL(1.5e12*1.71e-10, 1.6e9/1.5e12,'0')    # J14011+0252; Carilli+2005
UL(6.1e12*1.71e-10, 3.7/6.1e3,'0')    #J02396-0134
UL(1.5e12*1.71e-10, 1.6e9/1.5e12,'0')    # J14011+0252; Carilli+2005

for i in range(6):
    if R21_HCN[i]<0.0:
        pass
        #UL(R21_FIR[i]/R21_mu[i]*1.71e-10, -R21_HCN[i]/R21_FIR[i],'dodgerblue',100)
    else:
        plt.scatter(R21_FIR[i]/R21_mu[i]*1.71e-10,R21_HCN[i]/R21_FIR[i], color='dodgerblue',s = 100)
        plt.errorbar(R21_FIR[i]/R21_mu[i]*1.71e-10,R21_HCN[i]/R21_FIR[i], yerr = R21_HCN_err[i]/R21_FIR[i],color='dodgerblue')


# SDP.9
plt.text(1.08e13*1.71e-10,8.e-4,'SDP.9', color = '0', verticalalignment = 'center', ha='center')
plt.scatter(1.08e13*1.71e-10, 7.e-4, c='0', s=50, label = 'DSFGs , HCN(1-0)')


r_41 = 0.59
SMG_HCN/=r_41
for i in range(len(SMG_HCN)):
    if SMG_HCN[i]<0.0:
        UL(SMG_FIR[i]/SMG_mu[i]*1.71e-10, -SMG_HCN[i]/SMG_FIR[i],'royalblue',100)
    else:
        plt.scatter(SMG_FIR[i]/SMG_mu[i]*1.71e-10,SMG_HCN[i]/SMG_FIR[i], color='royalblue',s = 100)
        plt.errorbar(SMG_FIR[i]/SMG_mu[i]*1.71e-10,SMG_HCN[i]/SMG_FIR[i], yerr = SMG_HCN_err[i]/SMG_FIR[i],color='royalblue')

plt.scatter(1,1, color='royalblue',s = 100, label = 'DSFGs, HCN(4-3)')

print ("median = ", np.median(SMG_HCN[SMG_HCN>0]/SMG_FIR[SMG_HCN>0]), np.nanstd(SMG_HCN[SMG_HCN>0]/SMG_FIR[SMG_HCN>0]))

# calculate the significance of the offset:
SFE_dense = (SMG_HCN[SMG_HCN>0]/SMG_FIR[SMG_HCN>0])
print ("SFE_dense =", SFE_dense)
SFE_dense_rms = SFE_dense*np.sqrt(SMG_HCN_err[SMG_HCN>0]**2/SMG_HCN[SMG_HCN>0]**2)
Diff = 1e-3/SFE_dense
Diff_err = Diff*((10**-0.37)**2+SFE_dense_rms**2/SFE_dense**2)
print (Diff, Diff_err)
print (Diff/Diff_err)

plt.scatter(0.0001,0.0001, s=50, color = 'darkorange', label='Rybak+2022')
UL(6.0e12*1.71e-10, 3.7e-4, 'darkorange', 100)



# Jimenez-Donaire 2019
plt.plot([1.e8*1.71e-10, 1.e15*1.71e-10], [1./977., 1./977.], color='0', lw=0.5, linestyle = 'dashed')

plt.plot([1.e8*1.71e-10, 1.e15*1.71e-10], [1./977.*10**0.37, 1./977.*10**0.37], color='0', lw=0.5, linestyle = 'dashed')
plt.plot([1.e8*1.71e-10, 1.e15*1.71e-10], [1./977./10**0.37, 1./977./10**0.37], color='0', lw=0.5, linestyle = 'dashed')


#plt.fill_between([0.01,1e14*1.71e-10],[1e-6,1e-6],[1/977,1/977], fc='cornflowerblue', alpha=0.2, zorder=0)
#plt.fill_between([0.01,1e14*1.71e-10],[1/977,1/977],[1,1], fc='salmon', alpha=0.2, zorder=0)

#plt.text(0.15,0.009, "low SFE", c='salmon',fontsize=16,zorder=10, va='top')
#plt.text(0.15,0.001, "high SFE", c='royalblue',fontsize=16,zorder=10, va='top')


plt.legend(frameon=True, loc = 'lower left', fontsize =11)



ax2 = ax.twinx()
plt.yscale('log')
plt.ylim((10.0*1.e-4)/(1.71e-10)/1.e6, (10.0*1.e-2)/(1.71e-10)/1.e6)
#ax2.set_ylabel(r"t$_\mathrm{dep}$ = M$_\mathrm{dense}$/SFR [Myr]", fontsize = 13)
ax2.set_ylabel(r"t$_\mathrm{dep}$ [Myr]", fontsize = 13)
plt.tick_params(axis='both', which = 'major', length=10, direction = 'in', width=0.5, color = 'black', labelsize = 10)
plt.tick_params(axis='both', which = 'minor',length=5, direction = 'in', width=0.5, color = 'black', labelsize = 10)

plt.gcf().set_size_inches(6,5)

plt.savefig('fig_SFE_20250717.png', dpi = 200,bbox_inches='tight')
#plt.savefig('fig_FIR_HCN_over_FIR_wide_literature.png', dpi = 200, bbox_inches='tight')
