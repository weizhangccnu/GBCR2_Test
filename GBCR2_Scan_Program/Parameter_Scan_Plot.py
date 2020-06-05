import math
from matplotlib.pylab import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from matplotlib import rcParams
rcParams['font.family'] = 'Times New Roman'         # set the axis font.family
#================================================================================================#
## plot parameters
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#================================================================================================#
def Rx_parameter_plot(data):
    ax = plt.subplot(111)
    im = ax.imshow(data, cmap='jet')

    plt.title("GBCR2 Rx Channel Parameters Scan", family="Times New Roman", fontsize=12)
    plt.xlabel("MFSR[3:0]", family="Times New Roman", fontsize=10)
    plt.ylabel("HFSR[3:0]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='', linewidth=lw_grid)
    # plt.legend(fontsize=8, edgecolor='green')

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    cb = plt.colorbar(im, cax=cax, label="Jitter Histogram Std [ps]")
    cb.ax.tick_params(labelsize=8)
    # plt.ylabel("Jitter [ps]", family="Times New Roman", fontsize=10)
    plt.savefig("GBCR2_RX_Parameters_Scan.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()
# plt.show()
#================================================================================================#
def Tx_parameter_plot(data):
    ax = plt.subplot(111)
    im = ax.imshow(data, cmap='jet')

    plt.title("GBCR2 Tx Channel Parameters Scan", family="Times New Roman", fontsize=12)
    plt.xlabel("DL_SR[2:0],Dis_LPF_BIAS", family="Times New Roman", fontsize=10)
    plt.ylabel("DLL_ATT[1:0],Dis_DL_Emp", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='', linewidth=lw_grid)
    # plt.legend(fontsize=8, edgecolor='green')

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    cb = plt.colorbar(im, cax=cax, label="Jitter Histogram Std [ps]")
    cb.ax.tick_params(labelsize=8)
    # plt.ylabel("Jitter [ps]", family="Times New Roman", fontsize=10)
    plt.savefig("GBCR2_TX_Parameters_Scan.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()
#================================================================================================#
def main():
    data = [[] for x in range(16)]
    with open("Hist_Std_Dev.dat", 'r') as infile:
        i = 0
        for line in infile.readlines():
            print(i/16)
            data[math.floor(i/16)] += [float(line.split()[1])*1.0e12]
            i += 1
    Rx_parameter_plot(data)
    print(data)
    mim_item = min(min(row) for row in data)
    print(mim_item)

    data1 = [[] for x in range(8)]
    with open("TX_Hist_Std_Dev.dat", 'r') as infile:
        i = 0
        for line in infile.readlines():
            print(i/8)
            data1[math.floor(i/16)] += [float(line.split()[1])*1.0e12]
            i += 1
    print(data1)
    mim_item1 = min(min(row) for row in data1)
    print(mim_item1)
    Tx_parameter_plot(data1)
    print("Ok!!")
#================================================================================================#
if __name__ == '__main__':
    main()
