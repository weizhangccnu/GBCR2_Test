#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import copy
import time
import datetime
import struct
import socket
from usb_iss import UsbIss, defs
from GBCR2_Reg import *
import pyvisa as visa
from command_interpret import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
'''
@author: Wei Zhang
@date: 2020-11-14
This script is used to test GBCR2 SEU. It mainly includes I2C communication, Ethernet communication, and eight channels bit error record.
'''
hostname = '192.168.2.3'                # FPGA IP address
port = 1024                             # port number
#------------------------------------------------------------------------------------------------#
## IIC write slave device
# @param mode[1:0] : '0'is 1 bytes read or wirte, '1' is 2 bytes read or write, '2' is 3 bytes read or write
# @param slave[7:0] : slave device address
# @param wr: 1-bit '0' is write, '1' is read
# @param reg_addr[7:0] : register address
# @param data[7:0] : 8-bit write data
def iic_write(mode, slave_addr, wr, reg_addr, data):
    val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | data
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)           # reset ddr3 data fifo
    time.sleep(0.01)
#---------------------------------------------------------------------------------------------#
## IIC read slave device
# @param mode[1:0] : '0'is 1 bytes read or wirte, '1' is 2 bytes read or write, '2' is 3 bytes read or write
# @param slave[6:0]: slave device address
# @param wr: 1-bit '0' is write, '1' is read
# @param reg_addr[7:0] : register address
def iic_read(mode, slave_addr, wr, reg_addr):
    val = mode << 24 | slave_addr << 17 |  0 << 16 | reg_addr << 8 | 0x00     # write device addr and reg addr
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)                                     # Sent a pulse to IIC module

    val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | 0x00     # write device addr and read one byte
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)                                     # Sent a pulse to IIC module
    time.sleep(0.01)                                                          # delay 10ns then to read data
    return cmd_interpret.read_status_reg(0) & 0xff
#---------------------------------------------------------------------------------------------#
## Bit error record
# @param channel: 0-6 represents Rx channel 0-6, 7 represents Tx channel
# @return: channel bit error record number
def Bit_error_record():
    Bit_error_byte = []
    for i in range(8):
        time.sleep(0.05)
        cmd_interpret.write_config_reg(0, 0x0007 & i)
        for j in range(4):
            Bit_error_byte += [cmd_interpret.read_status_reg(4-j)]
    Channel_bit_error = []
    for i in range(8):
        Channel_bit_error += [Bit_error_byte[0+i*4]<<48 | Bit_error_byte[1+i*4]<<32 | Bit_error_byte[2+i*4]<<16 | Bit_error_byte[3+i*4]]
    return Channel_bit_error
#---------------------------------------------------------------------------------------------#
## soft clear all channels error bit count
# @param[in] val: 1: all channles error bit count will be cleared, 0: remains previous value
def soft_clear_error_bit_count(val):
    if val == 1:
        cmd_interpret.write_pulse_reg(0x0002)
#---------------------------------------------------------------------------------------------#
## Set Rx and Tx channels initial value
# @param[in] val: [Rx0_Init_Val, Rx1_Init_Val, Rx2_Init_Val, Rx3_Init_Val, Rx4_Init_Val, Rx5_Init_Val, Rx6_Init_Val, Tx0_Init_Val]
def Set_error_bit_init_value(val):
    cmd_interpret.write_config_reg(6, 0xffff & ((val[1]&0xff)<<8 | (val[0]&0xff)))
    cmd_interpret.write_config_reg(7, 0xffff & ((val[3]&0xff)<<8 | (val[2]&0xff)))
    cmd_interpret.write_config_reg(8, 0xffff & ((val[5]&0xff)<<8 | (val[4]&0xff)))
    cmd_interpret.write_config_reg(9, 0xffff & ((val[7]&0xff)<<8 | (val[6]&0xff)))
#---------------------------------------------------------------------------------------------#
## Current_Monitor
def Current_monitor():

    I2C_Addr = 0x9e >> 1                        # I2C address of first LTC2991, note that 

    iic_write(1, I2C_Addr, 0, 0x06, 0x99)       # V1-V2 differential, Filter enabled, V3-V4 differential, Filter enabled
    # print(iic_read(0, I2C_Addr, 1, 0x06))       # read back control register

    iic_write(1, I2C_Addr, 0, 0x01, 0x38)       # V1-V2 and V3-V4 enabled, VCC and T internal enabled

    # print(hex(iic_read(0, I2C_Addr, 1, 0x00)))  # status low 
    # print(hex(iic_read(0, I2C_Addr, 1, 0x01)))  # status high
    V12_Volt = 0
    I12 = 0
    V12_MSB = iic_read(0, I2C_Addr, 1, 0x0C)    # V1-V2 MSB
    V12_LSB = iic_read(0, I2C_Addr, 1, 0x0D)    # V1-V2 LSB
    V12_Valid = (V12_MSB & 0x80) >> 7
    V12_Sign = (V12_MSB & 0x40) >> 6
    if V12_Sign == 0: 
        V12_Volt = ((V12_MSB & 0x3f)<<8 | V12_LSB) * 19.075 * 1E-6
    I12 = 982.5 * V12_Volt -10.489
    print("V1-V2 volt: %.3f V, I12：%.3f mA"%(V12_Volt, I12))
    
    V34_Volt = 0
    I34 = 0
    V34_MSB = iic_read(0, I2C_Addr, 1, 0x10)    # V3-V4 MSB
    V34_LSB = iic_read(0, I2C_Addr, 1, 0x11)    # V3-V4 LSB
    V34_Valid = (V34_MSB & 0x80) >> 7
    V34_Sign = (V34_MSB & 0x40) >> 6
    if V34_Sign == 0: 
        V34_Volt = ((V34_MSB & 0x3f)<<8 | V34_LSB) * 19.075 * 1E-6
    I34 = 949.0 * V34_Volt + 0.0258
    print("V3-V4 volt: %.3f V, I34：%.3f mA"%(V34_Volt, I34))


    VCC_MSB = iic_read(0, I2C_Addr, 1, 0x1C)    # VCC MSB
    VCC_LSB = iic_read(0, I2C_Addr, 1, 0x1D)    # VCC LSB

    VCC_Volt = ((VCC_MSB & 0x3f)<<8 | VCC_LSB) * 0.00030518 + 2.5
    # print("VCC volt: %.3f"%VCC_Volt)
    return [I12, I34]
#---------------------------------------------------------------------------------------------#
def main():
    timeslot = int(sys.argv[1])                 # input time slot, unit is second
    Slave_Addr = 0x23

    # CH1_Delay = int(sys.argv[2])
    # Phase shifter settings
    GBCR2_Reg1.set_Rx_Enable(1)                 # enable eRx
    GBCR2_Reg1.set_Rx_setCM(1)
    GBCR2_Reg1.set_Rx_enTermination(1)
    GBCR2_Reg1.set_Rx_invData(0)
    GBCR2_Reg1.set_Rx_Equa(3)

    GBCR2_Reg1.set_Dis_Tx(0)

    GBCR2_Reg1.set_dllEnable(1)                 # enable DLL
    GBCR2_Reg1.set_dllCapReset(0)               # DLL cap reset
    GBCR2_Reg1.set_dllForceDown(0)
    GBCR2_Reg1.set_dllChargePumpCurrent(15)


    GBCR2_Reg1.set_dllClockDelay_CH0(6)
    GBCR2_Reg1.set_dllClockDelay_CH1(6)
    GBCR2_Reg1.set_dllClockDelay_CH2(6)
    GBCR2_Reg1.set_dllClockDelay_CH3(6)
    GBCR2_Reg1.set_dllClockDelay_CH4(6)
    GBCR2_Reg1.set_dllClockDelay_CH5(6)
    GBCR2_Reg1.set_dllClockDelay_CH6(6)
    GBCR2_Reg1.set_dllClockDelay_CH7(6)


    # Rx channel 1 settings
    GBCR2_Reg1.set_CH1_CML_AmplSel(7)
    GBCR2_Reg1.set_CH1_CTLE_MFSR(10)
    GBCR2_Reg1.set_CH1_CTLE_HFSR(7)
    GBCR2_Reg1.set_CH1_Dis_DFF(1)               # 1: equalizer mode, 0: retiming mode

    # Rx channel 2 settings
    GBCR2_Reg1.set_CH2_CML_AmplSel(7)
    GBCR2_Reg1.set_CH2_CTLE_MFSR(10)
    GBCR2_Reg1.set_CH2_CTLE_HFSR(7)
    GBCR2_Reg1.set_CH2_Dis_DFF(1)               # 1: equalizer mode, 0: retiming mode

    # Rx channel 3 settings
    GBCR2_Reg1.set_CH3_CML_AmplSel(7)
    GBCR2_Reg1.set_CH3_CTLE_MFSR(10)
    GBCR2_Reg1.set_CH3_CTLE_HFSR(7)
    GBCR2_Reg1.set_CH3_Dis_DFF(1)               # 1: equalizer mode, 0: retiming mode

    # Rx channel 4 settings
    GBCR2_Reg1.set_CH4_CML_AmplSel(7)
    GBCR2_Reg1.set_CH4_CTLE_MFSR(10)
    GBCR2_Reg1.set_CH4_CTLE_HFSR(7)
    GBCR2_Reg1.set_CH4_Dis_DFF(1)               # 1: equalizer mode, 0: retiming mode

    # Rx channel 5 settings
    GBCR2_Reg1.set_CH5_CML_AmplSel(7)
    GBCR2_Reg1.set_CH5_CTLE_MFSR(10)
    GBCR2_Reg1.set_CH5_CTLE_HFSR(7)
    GBCR2_Reg1.set_CH5_Dis_DFF(1)               # 1: equalizer mode, 0: retiming mode

    # Rx channel 6 settings
    GBCR2_Reg1.set_CH6_CML_AmplSel(7)
    GBCR2_Reg1.set_CH6_CTLE_MFSR(10)
    GBCR2_Reg1.set_CH6_CTLE_HFSR(7)
    GBCR2_Reg1.set_CH6_Dis_DFF(1)               # 1: equalizer mode, 0: retiming mode

    # Rx channel 7 settings
    GBCR2_Reg1.set_CH7_CML_AmplSel(7)
    GBCR2_Reg1.set_CH7_CTLE_MFSR(10)
    GBCR2_Reg1.set_CH7_CTLE_HFSR(7)
    GBCR2_Reg1.set_CH7_Dis_DFF(1)               # 1: equalizer mode, 0: retiming mode

    # Tx channel 1 settings
    GBCR2_Reg1.set_Tx1_Dis_DL_BIAS(0)
    GBCR2_Reg1.set_Tx1_Dis_DL_LPF_BIAS(0)

    iic_write_val = GBCR2_Reg1.get_config_vector()

    ## soft clear error bit count
    soft_clear_error_bit_count(1)

    ## Set_error_bit_init_value
    channel_bit_error_init_val = [0, 0, 0, 0, 0, 0, 0, 0]
    Set_error_bit_init_value(channel_bit_error_init_val)

    print(iic_write_val)
    ## write data into I2C register one by one
    for i in range(len(iic_write_val)):
        iic_write(1, Slave_Addr, 0, i, iic_write_val[i])

    iic_read_val = []
    ## read back  data from I2C register one by one
    for i in range(len(iic_write_val)):
        iic_read_val += [iic_read(0, Slave_Addr, 1, i)]
    print(iic_read_val)

    if iic_read_val == iic_write_val:
        print("Wrote into data matches with read back data!")
    else:
        print("Wrote into data doesn't match with read back data!")

    ## channel bit error write into file
    today = datetime.date.today()
    print(today)

    Channel_bit_error = []
    Previous_Channel_bit_error = []
    lasttime = datetime.datetime.now()
    with open("./Log_file/GBCR2_bit_error_%s.txt"%(today), 'a') as infile1, open("./Log_file/GBCR2_bit_error_location_%s.txt"%(today), 'a') as infile2, open("./Log_file/GBCR2_Current_Monitor_%s.txt"%(today), 'a') as infile3:
        while True:
            if(datetime.datetime.now() - lasttime > datetime.timedelta(seconds=timeslot)):
                lasttime = datetime.datetime.now()
                Channel_bit_error = Bit_error_record()
                print(lasttime, Channel_bit_error)
                infile1.write("%s %15d %15d %15d %15d %15d %15d %15d %15d\n"%(lasttime, Channel_bit_error[0], Channel_bit_error[1], Channel_bit_error[2], Channel_bit_error[3],\
                 Channel_bit_error[4], Channel_bit_error[5], Channel_bit_error[6], Channel_bit_error[7]))
                if Channel_bit_error != Previous_Channel_bit_error:
                    infile2.write("%s %15d %15d %15d %15d %15d %15d %15d %15d\n"%(lasttime, Channel_bit_error[0], Channel_bit_error[1], Channel_bit_error[2], Channel_bit_error[3],\
                     Channel_bit_error[4], Channel_bit_error[5], Channel_bit_error[6], Channel_bit_error[7]))
                Previous_Channel_bit_error = Channel_bit_error
                current = Current_monitor()
                infile3.write("%s %.3f %.3f\n"%(lasttime, current[0], current[1]))
                infile1.flush()                 # write data into file one by one
                infile2.flush()
                infile3.flush()

    print("Ok!")
#------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # initial socket
    s.connect((hostname, port))                             # connect socket
    cmd_interpret = command_interpret(s)                    # Class instance
    GBCR2_Reg1 = GBCR2_Reg()                                # New a class
    main()                                                  # execute main function
    s.close()                                               # close socket
