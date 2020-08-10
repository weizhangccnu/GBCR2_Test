## GBCR2 Quality Control
  - GBCR2 is a gigabit transceiver prototype ASIC for the ATLAS phase-II upgrade of the ITK pixel detector front-end electrical links. It has seven uplink channels that recieve 1.28 Gbps signals and two downlink channels that send 160 Mbps  signals.
  - Test Instrument:
    - Pattern Generator: **Tektronix DGT5274**
    - Oscilloscope: **Tektronix DSA70804B (Bandwidth=8 GHz and Sample rate=25 Gsps)**
    - I2C Controller: **USB-iss module**
    - Switch Controller: **LabJack U3-HV**
    - High Speed Switch: **HMC321ALP4E**
### 1. File orangization
  - **GBCR2_QC_Software:** save QC test python script.
  - **./GBCR2_QC_Software/GBCR2_Test_Log:** save each tested chip log file.
### 2. How to execute `./GBCR2_QC_Software/GBCR2_QC_Test_Control.py`
  - using`python ./GBCR2_QC_Test_Control.py Test_Channel Tester_Name Chip_ID` command in the GBCR2_QC_Software directory.
  - Test_Channel: Rx or Tx
  - Tester_Name: your name
  - Chip_ID: from 001 to 175
  - Example: **`python ./GBCR2_QC_Test_Control.py Rx Wei 001`** to test NO.001 chip all Rx channels by Wei  
### 3. Log will be created after each test.
  - GBCR2_QC_**TestMode**_**Chip_ID**.txt for exampel: `GBCR2_QC_Rx_001.txt`
    * TestMode: Rx or Tx
    * Chip_ID: 001 to 175
  - What will be recorded in log file
    * Test start time
    * Tester name
    * I2C communication status
    * Power current in different power  voltage
    * The amplitude, RMS Jitter, Rise time, Fall Time of Eye-diagram under different power supply (1.08V, 1.2V and 1.32V)
### 4. Eye-diagram will be saved to C:/GBCR2_QC_Test directoty on OSC (Tektronix DSA70804B)
  * Chip_ID=xxx_RX_CHx_VDD=xx_Eye-diagram_Img.png for Rx Channels
    - Chip_ID: 001 to 1175
    - Channel ID: 1 to 7
    - VDD: 1V08, 1V20, and 1V32.
  * Chip_ID=xxx_TX_CHx_VDD=xx_Eye-diagram_Img.png for Tx Channels
    - Chip_ID: 001 to 1175
    - Channel ID: 1 to 2
    - VDD: 1V08, 1V20, and 1V32.

