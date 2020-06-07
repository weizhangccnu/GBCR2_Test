#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import copy
import time
import visa
import winsound
import datetime
import struct
import socket
from usb_iss import UsbIss, defs
from GBCR2_Reg import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
#========================================================================================#
freqency = 1000
duration = 1000
'''
@author: Wei Zhang
@date: 2020-06-03
This script is used for testing GBCR2 chip.
'''
#------------------------------------------------------------------------------------------------#
def capture_screen_image(filename):
    rm = visa.ResourceManager()
    print(rm.list_resources())
    inst = rm.open_resource('GPIB2::7::INSTR')              # connect to SOC
    # print(inst.query("*IDN?"))                              # Instrument ID
    # time.sleep(0.5)

    inst.write("*RST")                                      # reset OSC
    time.sleep(3)

    inst.write(":CHANnel1:DIFFerential ON")                 # Channel 1 and channel 3 differential mode

    inst.write(":AUToscale:VERTical CHAN1")
    # time.sleep(1)

    inst.write(":TIMebase:RANGe 2E-9")
    # time.sleep(1)

    inst.write(":TRIGger:MODE EDGE")                        # set trigger mode
    # print(inst.query(":TRIGger:MODE?"))
    inst.write(":TRIGger:EDGE:SOURce CHANnel2")             # channel2 is set to Edge trigger source

    inst.write(":DISPlay:PERSistence INFinite")             # Display Persistence Infinite

    # print(inst.query(":HISTogram:MODE?"))
    # time.sleep(1)
    inst.write(":HISTogram:MODE WAVeform")                  # Histogram mode waveform
    time.sleep(0.5)
    inst.write(":HISTogram:AXIS HORizontal")                # Histogram horizontal
    time.sleep(0.5)
    inst.write(":HISTogram:WINDow:SOURce CHANnel1")         # windown source Channel1
    # time.sleep(0.5)
    inst.write(":HISTogram:WINDow:LLIMit -600E-12")         #
    # time.sleep(0.5)
    inst.write(":HISTogram:WINDow:RLIMit 200E-12")
    # time.sleep(1)
    inst.write(":HISTogram:WINDow:BLIMit -1E-3")
    # time.sleep(0.5)
    inst.write(":HISTogram:WINDow:TLIMit 1E-3")
    time.sleep(50)


    Hist_Std_Dev = inst.query(":MEASure:HISTogram:STDDev? HISTogram")
    time.sleep(0.5)

    inst.write(':DISK:CDIRectory "D:\GBCR2_Scan_20200605_Chufeng"')         # set screen image store directory
    # inst.write(':DISK:MDIRectory "D:\GBCR2_Scan_20200604"')       # make a directory
    # print(inst.query(":DISK:PWD?"))                                 # current direcotry
    time.sleep(0.5)
    inst.write(':DISK:SAVE:IMAGe "%s",BMP,SCReen'%filename)         # save screen image
    return Hist_Std_Dev
#---------------------------------------------------------------------------------------------#
def main():
    rm = visa.ResourceManager()
    inst1 = rm.open_resource('USB0::0x2A8D::0x1102::MY58041595::0::INSTR')      # top power supply
    inst1.write("*RST")
    inst1.write("SOURce:VOLTage 1.2,(@1)")                                      # top channel 1
    inst1.write("SOURce:CURRent 0.2,(@1)")
    inst1.write("OUTPut:STATe ON,(@1)")                                         # enable bottom channel 1
    time.sleep(2)
    iss = UsbIss()
    iss.open("COM3")
    iss.setup_i2c(clock_khz=100, use_i2c_hardware=True, io1_type=None, io2_type=None)
    I2C_Addr = 0X23
    Chip_ID = int(sys.argv[1])
    print("Chip %d is being testing!!!"%Chip_ID)
    CH_ID = 4
    GBCR2_Reg1 = GBCR2_Reg()
    CH_Dis_Rx = 0
    CH_CML_AmplSel = 5
    CH_Dis_EQ_LF = 0
    CH_EQ_ATT = 3
    CH_CTLE_HFSR = 7
    CH_CTLE_MFSR = 10
    CH_Dis_DFF = 1
    CH_Dis_LPF = 0

    GBCR2_Reg1.set_CH4_CML_AmplSel(CH_CML_AmplSel)
    GBCR2_Reg1.set_CH4_CTLE_MFSR(CH_CTLE_MFSR)
    GBCR2_Reg1.set_CH4_CTLE_HFSR(CH_CTLE_HFSR)
    filename = "Chip=%1d_CH%1d_Dis_Rx=0_CML_AmplSel=%1d_Dis_EQ_LF=0_EQ_ATT=3_CTLE_HFSR=%02d_CTLE_MFSR=%02d_Dis_DFF=1_Dis_LPF=0"%(Chip_ID,CH_ID,CH_CML_AmplSel,CH_CTLE_HFSR,CH_CTLE_MFSR)
    print(filename)
    Reg_Write_val = GBCR2_Reg1.get_config_vector()
    print(Reg_Write_val)
    iss.i2c.write(I2C_Addr, 0, Reg_Write_val)
    Reg_Read_val = []
    Reg_Read_val = iss.i2c.read(I2C_Addr, 0, 0x20)
    print("GBCR2 I2C Read Back data:")
    print(Reg_Read_val)
    print("\n")
    Hist_Std_Dev = capture_screen_image(filename)
    time.sleep(1)
    # inst1.write("OUTPut:STATe OFF,(@1)")                                         # enable bottom channel 1
    winsound.Beep(freqency, duration)
#------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
