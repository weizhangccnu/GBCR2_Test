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
    iss = UsbIss()
    iss.open("COM8")
    iss.setup_i2c()
    print("Ok!!!")
#=======================================================================================#
if __name__ == '__main__':
    main()
