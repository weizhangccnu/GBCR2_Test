## GBCR2 Quality Control
### 1. File orangization
  - **GBCR2_QC_Software:** save QC test python script.
  - **./GBCR2_QC_Software/GBCR2_Test_Log:** save each tested chip log file.
### 2. How to execute `./GBCR2_QC_Software/GBCR2_QC_Test_Control.py`
  - using`python ./GBCR2_QC_Test_Control.py Test_Channel Tester_Name Chip_ID` command in the GBCR2_QC_Software directory.
  - Test_Channel: Rx or Tx
  - Tester_Name: your name
  - Chip_ID: from 001 to 175
  - Example: **`python ./GBCR2_QC_Test_Control.py Rx Wei 001`** to test NO.001 chip all Rx channels by Wei  
### 3. Eye-diagram is save to C:/GBCR2_QC_Test directoty on OSC (Tektronix DSA70804B)
  * Chip_ID=xxx_RX_CHx_VDD=xx_Eye-diagram_Img.png for Rx Channels
    - Chip_ID: 001 to 1175
    - Channel ID: 1 to 7
    - VDD: 1V08, 1V20, and 1V32.
  * Chip_ID=xxx_TX_CHx_VDD=xx_Eye-diagram_Img.png for Tx Channels
    - Chip_ID: 001 to 1175
    - Channel ID: 1 to 2
    - VDD: 1V08, 1V20, and 1V32.

