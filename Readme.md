## 1. USB-ISS multifunction USB communications module
  - [technical specification link](https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm)
## 2. Python library for the USB-ISS board
  - [USB ISS Python Module Introduction](https://usb-iss.readthedocs.io/en/latest/)
  - Install `usb-iss` module via `pip` command:
  ```python
  pip install usb-iss
  ```
## 3. Convert xxx.ui to xxx.py
  - Use the command `C:\Users\47859153\AppData\Local\Programs\Python\Python37\Scripts\pyuic5 -x GBCR2_Test_GUI.ui -o GBCR2_Test_GUI.py` convert .ui file into .py file.
## 4. Using pyinstaller generates executable file from .py file
```
pyinstaller -Fw GBCR2_Test_GUI.py         # F: one File     w: without console
```
## 5. The GBCR2 Test Gui is show as below picture
  - ![GBCR2 Test Gui](https://github.com/weizhangccnu/GBCR2_Test/blob/master/Img/GBCR2_Test_Gui.PNG)
