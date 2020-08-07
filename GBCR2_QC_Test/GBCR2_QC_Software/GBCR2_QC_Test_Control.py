import os
import sys
import time
from usb_iss import UsbIss, defs
'''
@author: Wei Zhang
@date: March 2rd, 2020
This python script is used to control the GBCR2 I2C slave.
'''
#=======================================================================================#
def main():
    ## set usb-iss iic master device
    slave_addr = 0x23
    iss = UsbIss()
    iss.open("COM3")
    iss.setup_i2c()

    ## GBCR2 Register mapping 


    iss.i2c.write(slave_addr, 0, [0, 1, 2])

    data = iss.i2c.read(slave_addr, 0, 3)
    print(data)
    print("Ok!!!")
#=======================================================================================#
if __name__ == '__main__':
    main()
