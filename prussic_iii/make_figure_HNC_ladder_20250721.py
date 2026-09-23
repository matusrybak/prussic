
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






def main():

    table_dict = read_table_as_dict('../MasterTableLines_20250717.csv')

    SMG_ID = table_dict['Source_ID']
    SMG_HNC10 = np.asarray(table_dict['HNC(1-0)'])
    SMG_HNC10_rms = np.asarray(table_dict['Delta_HNC(1-0)'])
    SMG_HNC32 = np.asarray(table_dict['HNC(3-2)'])
    SMG_HNC32_rms = np.asarray(table_dict['Delta_HNC(3-2)'])
    SMG_HNC43 = np.asarray(table_dict['HNC(4-3)'])
    SMG_HNC43_rms = np.asarray(table_dict['Delta_HNC(4-3)'])

    Table  = open('HNC_ladders_Israel_2023.data')
    I2023_ID, I2023_FIR, I2023_HNC10, I2023_HNC32= np.genfromtxt(Table, unpack=True)
    Table.close()
    I2023_HNC3210 = I2023_HNC32/I2023_HNC10

    print (stats.scoreatpercentile(I2023_HNC3210, 50),stats.scoreatpercentile(I2023_HNC3210, 16),stats.scoreatpercentile(I2023_HNC3210, 84))
    # 0.343 0.252 0.802


    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.ylabel(r"$r_{j1}$", fontsize = 13)
    plt.xlabel(r"J$_\mathrm{upp}$", fontsize = 13)

    plt.tick_params(axis='both', which = 'major', length=10, direction = 'in', width=0.5, color = 'black', labelsize = 12)
    plt.tick_params(axis='both', which = 'minor',length=5, direction = 'in', width=0.5, color = 'black', labelsize = 12)

    plt.yscale('log')
    plt.xlim(0.5, 5)
    plt.ylim(5e-2, 2)


    for i in range(len(I2023_ID)):
        plt.plot([1,3],[1, I2023_HNC3210[i]], lw=1, c='0.66')


    # Israel+2023, MEDIAN values
    plt.plot([1,3], [1,0.32], c='0.33', lw=3, ls='dotted')
    plt.fill_between([1,3], [1,0.38],[1,0.26], fc='0.66',alpha=0.5)
    plt.text(3.1,1.6/5.2, "NGC6946",c='0.5')
    plt.text(3.1,31/45+0.04, "NGC253",c='0.5')
    plt.text(3.1,8.9/13.4-0.04, "NGC1068",c='0.5')


    #J1202
    j=SMG_ID.index('J1202')
    clr = 'orange'
    LL(3,-SMG_HNC32[j]/SMG_HNC10[j],clr,'0')
    plt.plot([1,3],[1, -SMG_HNC32[j]/SMG_HNC10[j]],lw=2,ls='dashed',c=clr)
    print (-SMG_HNC32[j]/SMG_HNC10[j])

    #J0209
    j=SMG_ID.index('J0209')
    clr = 'deepskyblue'
    plt.errorbar(3,SMG_HNC32[j]/SMG_HNC10[j],yerr = SMG_HNC32[j]/SMG_HNC10[j]*np.sqrt(SMG_HNC32_rms[j]**2/SMG_HNC32[j]**2+SMG_HNC10_rms[j]**2/SMG_HNC10[j]**2), c=clr,zorder=5,lw=2)
    plt.errorbar(4,SMG_HNC43[j]/SMG_HNC10[j],yerr = SMG_HNC43[j]/SMG_HNC10[j]*np.sqrt(SMG_HNC43_rms[j]**2/SMG_HNC43[j]**2+SMG_HNC10_rms[j]**2/SMG_HNC10[j]**2), c=clr,zorder=5,lw=2)
    plt.scatter(3,SMG_HNC32[j]/SMG_HNC10[j],fc=clr,ec='0',zorder=5)
    plt.scatter(4,SMG_HNC43[j]/SMG_HNC10[j],fc=clr,ec='0',zorder=5)
    plt.plot([1,3,4],[1, SMG_HNC32[j]/SMG_HNC10[j],SMG_HNC43[j]/SMG_HNC10[j]],lw=2,ls='dashed',c=clr)

    #SDP.9
    j=SMG_ID.index('SDP.9')
    clr = 'dodgerblue'
    LL(3,-SMG_HNC32[j]/SMG_HNC10[j],clr,'0')
    LL(4,-SMG_HNC43[j]/SMG_HNC10[j],clr,'0')
    plt.plot([1,3,4],[1, -SMG_HNC32[j]/SMG_HNC10[j],-SMG_HNC43[j]/SMG_HNC10[j]],lw=2,ls='dashed',c=clr)


    #SDP.130
    j=SMG_ID.index('SDP.130')
    clr = 'orangered'
    #LL(3,-SMG_HNC32[j]/SMG_HNC10[j],clr,'0')
    LL(4,-SMG_HNC43[j]/SMG_HNC10[j],clr,'0')
    plt.plot([1,4],[1,-SMG_HNC43[j]/SMG_HNC10[j]],lw=2,ls='dashed',c=clr)



    #plt.text(0.7,0.07*1.2**4,"J16359",c='darkorange')
    plt.text(0.7,0.07*1.2**3,"J1202",c='orange')
    plt.text(0.7,0.07*1.2**2,"J0209",c='deepskyblue')
    plt.text(0.7,0.07*1.2,"SDP.9",c='dodgerblue')
    plt.text(0.7,0.07,"SDP.130",c='orangered')
    plt.text(0.6,1.5,r"HNC",fontsize=18)
    plt.gcf().set_size_inches(5,5)
    plt.savefig('fig_HNC_ladders_202507.png', dpi = 150, bbox_inches='tight')




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


main()
