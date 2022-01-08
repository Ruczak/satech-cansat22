# Satech Cansat
### Edition 2021/22
<img src="https://drive.google.com/uc?export=view&id=1Y8iNRtcaDI3GDSQ605UacmiUN2jqexMc" style="height: 300px; max-height: 100%; width: auto" /><br>
## Introduction
This is source code of a **SaTech's CanSat**.
## Installation

1. Check for updates :
```
sudo apt-get update
sudo apt-get upgrade
```
2. Install git: ``sudo apt-get install git``
3. Copy repo with: ``git clone https://github.com/Ruczak/satech-cansat22.git``
4. Make sure you have python3 installed: ``sudo python3``
5. Install package installer for python (PIP) ``sudo apt-get install python-pip``
6. Install required dependencies: ``sudo apt-get install python-smbus python-serial``
7. Install required python libraries: ``sudo python3 -m pip install RPi.GPIO csv``
8. Open serial port with:
    1. Type in terminal: ``sudo raspi-config``
    2. Select **Interface Options**
    3. Select **Serial Port**
    4. Select **No** when asked *Would you like a login shell to be accessible over serial?*
    5. Select **Yes** when asked *Would you like the serial port hardware to be enabled?*
    6. Select **Ok**
    7. Select **Finish**
9. Reboot with ``sudo reboot`` 
