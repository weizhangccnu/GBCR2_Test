import os
import sys
import visa
from u3 import *
import time
from GBCR2_Reg import *
from labjack import ljm
from usb_iss import UsbIss, defs
'''
@author: Wei Zhang
@date: March 2rd, 2020
This python script is used to control the GBCR2 I2C slave.
'''
#=======================================================================================#
## Power Supply Control
# @param[in]: Instrument Handle
# @param[in]: Power Voltage input
# return: Channel_One_Current
def Power_Control(Inst, Channel_One_Volt):

    Inst.write("OUTPut:STATe ON,(@1)")                                    # Turn On Power Channel One
    Inst.write("SOURce:VOLTage %.2f,(@1)"%(Channel_One_Volt))             # Channel One Power Voltage
    Channel_One_Current = round(float(Inst.query("MEAS:CURR? CH1"))*1000.0, 3)
    return Channel_One_Current
#=======================================================================================#
## Capture Screen Image
def Capture_Screen_Image(inst, filename):
    inst.write("*RST")                                      # reset the OSC
    time.sleep(8)
    inst.write("ACQuire:SAMPlingmode ET")                   # Acquire samplinng mode : Equivalent Time
    time.sleep(0.01)
    inst.write("TRIGGER:A:EDGE:SOURCE CH1")                 # set tirgger source and edge
    inst.write("HORIZONTAL:DELAY:MODE ON")                  # set Delay MODE
    inst.write("HORIZONTAL:DELAY:TIMe 1.88E-8")             # set Delay MODE

    inst.write("HORizontal:MODE:SCAle 2E-9")                # set horizontal scale
    inst.write("DISplay:PERSistence INFPersist")
    inst.write("CH1:SCAle 5.0E-2")
    # print(inst.query("CH1:SCAle?"))

    inst.write("HIStogram:MODe HORizontal")
    inst.write("HIStogram:SOUrce CH1")
    inst.write("HIStogram:DISplay LINEAr")
    inst.write("HIStogram:BOXPcnt 30, 49.75, 70, 50.25")

    inst.write("MEASUrement:MEAS1:SOUrce1 HIStogram")
    inst.write("MEASUREMENT:MEAS1:TYPE STDdev")

    inst.write("MEASUrement:MEAS2:SOUrce1 CH1")
    inst.write("MEASUREMENT:MEAS2:TYPE AMPlitude")

    inst.write("MEASUrement:MEAS3:SOUrce1 CH1")
    inst.write("MEASUREMENT:MEAS3:TYPE RISe")

    inst.write("MEASUrement:MEAS4:SOUrce1 CH1")
    inst.write("MEASUREMENT:MEAS4:TYPE FALL")

    # inst.write("MEASUrement:MEAS2:SOUrce1 HIStogram")
    # inst.write("MEASUREMENT:MEAS2:TYPE PK2Pk")


    inst.write("MEASUrement:MEAS1:STATE ON")                # display frequency measurement results
    inst.write("MEASUrement:MEAS2:STATE ON")                # display rising edge measurement results
    inst.write("MEASUrement:MEAS3:STATE ON")                # display frequency measurement results
    inst.write("MEASUrement:MEAS4:STATE ON")                # display rising edge measurement results
    time.sleep(20)

    RMS_Jitter = inst.query("MEASUREMENT:MEAS1:VALue?")
    Amplitude = inst.query("MEASUREMENT:MEAS2:VALue?")
    Rise = inst.query("MEASUREMENT:MEAS3:VALue?")
    Fall = inst.query("MEASUREMENT:MEAS4:VALue?")

    inst.write("EXPort:FORMat PNG")                         # set export image format
    inst.write("EXPort:VIEW FULLSCREEN")                    # view range
    inst.write("EXPort:PALEtte COLOr")                      # palette full color
    inst.write("EXPort:FILEName 'C:\\GBCR2_QC_Test\\%s.PNG'"%filename)      # file store desitination
    inst.write("EXPort STARt")                              # start exprot image
    # print(inst.query("EXPort?"))                            # query export destination
    return [RMS_Jitter, Amplitude, Rise, Fall]

#=======================================================================================#
## I2C write and Read
def I2C_Write_Read(GBCR2_Reg1, iss):
    slave_addr = 0x23
    reg_val = []
    reg_val = GBCR2_Reg1.get_config_vector()
    # print(reg_val)
    iss.i2c.write(slave_addr, 0, reg_val)
    time.sleep(0.1)
    iic_read_reg = iss.i2c.read(slave_addr, 0, len(reg_val))
    # print(iic_read_reg)
    if reg_val == iic_read_reg:
        # print("Read back data matches with Write into data")
        I2C_Status = "Pass"
    else:
        # print("Read back data didn't matche with Write into data")
        I2C_Status = "Fail"
    return [I2C_Status, reg_val, iic_read_reg]

#=======================================================================================#
def main():

    ## Input Parameters
    Test_Mode = sys.argv[1]                 # Rx or Tx
    Tester_Name = sys.argv[2]               # Tester Name
    Chip_ID = sys.argv[3]                   # Chip id

    ## Power Supply
    rm = visa.ResourceManager()
    print(rm.list_resources())
    Power_Inst = rm.open_resource('USB0::0x2A8D::0x1002::MY59001324::INSTR')    # connect to SOC
    print(Power_Inst.query("*IDN?"))

    OSC_Inst = rm.open_resource('GPIB0::1::INSTR')                              # connect to SOC
    print(OSC_Inst.query("*IDN?"))

    ## set usb-iss iic master device
    slave_addr = 0x23
    iss = UsbIss()
    iss.open("COM8")
    iss.setup_i2c()

    ## Labjack instrument
    d = U3()
    # print(d.configU3())
    # print(d.configIO())

    GBCR2_Reg1 = GBCR2_Reg()

    with open("./GBCR2_Test_Log/GBCR2_QC_%s_Chip_ID=%s.txt"%(Test_Mode, Chip_ID), 'a+') as infile:
        time_stamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        infile.write("\n")
        infile.write("%s\n"%time_stamp)
        infile.write("%s\n"%Tester_Name)

        Channel_One_Current = Power_Control(Power_Inst, 1.277)                                    # Set Power Voltage is about 1.2 V
        infile.write("VDD=%.3fV IDD=%.3fA\n"%(1.2, Channel_One_Current))

        ## I2C write and read 10 times. if yes,
        loop_num = 0
        I2C_Status = "Fail"
        while(loop_num < 10 and I2C_Status == "Fail"):
            # print(loop_num)
            I2C_Status1 = I2C_Write_Read(GBCR2_Reg1, iss)
            I2C_Status = I2C_Status1[0]
            if I2C_Status == "Fail":
                infile.write("I2C Test Failed  %d\n"%loop_num)
                infile.write("Written values:\n")
                infile.writelines("%d "% val for val in I2C_Status1[1])
                infile.write("\n")
                infile.write("Read values:\n")
                infile.writelines("%d "% val for val in I2C_Status1[2])
                infile.write("\n")
                ## write iic write into data and read back data to file
            time.sleep(0.1)
            loop_num += 1
            if loop_num <= 10:
                infile.write("I2C Test Pass  %d\n"%loop_num)
                # infile.writelines("%d "% val for val in I2C_Status1[1])
                # infile.write("\n")
                # infile.writelines("%d "% val for val in I2C_Status1[2])
                # infile.write("\n")
            else:
                infile.write("I2C Test Failed  %d\n"%loop_num)
                infile.writelines("%d "% val for val in I2C_Status1[1])
                infile.write("\n")
                infile.writelines("%d "% val for val in I2C_Status1[2])
                infile.write("\n")
                ## write iic write into data and read back data to file
        Power_Volt = [1.277, 1.277, 1.411]
        Power_Volt_Board = [1.2, 1.08, 1.32]
        Channel_One_Current = []
        I2C_Status = []
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        for Volt in range(len(Power_Volt)):
            print("%.2fV Voltage Test......"%Power_Volt_Board[Volt])
            Channel_One_Current += [Power_Control(Power_Inst, Power_Volt[Volt])]
            print("Power Current: %.3f"%Channel_One_Current[Volt])
            time.sleep(1)
            I2C_Status += [I2C_Write_Read(GBCR2_Reg1, iss)[0]]
            print("I2C Status: %s"%I2C_Status[Volt])
            infile.write("%.2fV Voltage Test:==============================================\n"%Power_Volt_Board[Volt])
            infile.write("Power Current: %.3f\n"%Channel_One_Current[Volt])
            infile.write("I2C Status: %s\n"%I2C_Status[Volt])
            measured_items = []
            if Test_Mode == "Rx":
                for Chan in range(2):
                    print("Rx Channel %d is being tested!"%(Chan+1))
                    d.setFIOState(5, state = Chan & 0x1)
                    d.setFIOState(6, state = (Chan & 0x2) >> 1)
                    d.setFIOState(7, state = (Chan & 0x4) >> 2)
                    time.sleep(0.001)
                    Measure_Value = Capture_Screen_Image(OSC_Inst, "Chip_ID=%s_RX_CH%d_Img"%(Chip_ID, Chan+1))
                    print(Measure_Value)
                    infile.write("Rx Channel %d:######################\n"%(Chan+1))
                    infile.write("RMS Jitter: %.3f ps\n"%float(Measure_Value[0].split("E")[0]))
                    infile.write("Amplitude: %.3f mV\n"%float(Measure_Value[1].split("E")[0]))
                    infile.write("Rise Time: %.3f ps\n"%float(Measure_Value[2].split("E")[0]))
                    infile.write("Fall Time: %.3f ps\n"%float(Measure_Value[3].split("E")[0]))
            else:
                for Chan in range(2):
                    print("Tx Channel %d is being tested!"%(Chan+1))
                    d.setFIOState(5, state = Chan & 0x1)
                    d.setFIOState(6, state = (Chan & 0x2) >> 1)
                    d.setFIOState(7, state = (Chan & 0x4) >> 2)
                    time.sleep(0.001)
                    Measure_Value = Capture_Screen_Image(OSC_Inst, "Chip_ID=%s_TX_CH%d_Img"%(Chip_ID, Chan+1))
                    print(Measure_Value)
                    infile.write("Tx Channel %d:######################\n"%(Chan+1))
                    infile.write("RMS Jitter: %.3f ps\n"%float(Measure_Value[0]))
                    infile.write("Amplitude: %.3f mV\n"%float(Measure_Value[1]))
                    infile.write("Rise Time: %.3f ps\n"%float(Measure_Value[2]))
                    infile.write("Fall Time: %.3f ps\n"%float(Measure_Value[3]))
        print(Channel_One_Current)
        print(max(Channel_One_Current))
        print(min(Channel_One_Current))
        print(I2C_Status)

        if max(Channel_One_Current) < 180 and min(Channel_One_Current) > 45 and ("Fail" in I2C_Status) == False:
            print("Chip Test Pass")
            infile.write("Chip Test Pass\n\n")
        else:
            print("Chip Test didn't Pass")
            infile.write("Chip Test didn't Pass\n\n")

    ## Turn off Power
    Power_Inst.write("OUTPut:STATe OFF,(@1)")
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

#=======================================================================================#
if __name__ == '__main__':
    main()
