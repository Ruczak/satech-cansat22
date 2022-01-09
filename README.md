# SaTech Cansat

### Edition 2021/22

<img src="https://drive.google.com/uc?export=view&id=1Y8iNRtcaDI3GDSQ605UacmiUN2jqexMc" style="height: 300px; max-height: 100%; width: auto" /><br>

## Introduction

This is source code of a **SaTech's CanSat**.

## Installation

1. Check for updates

```
sudo apt-get update
sudo apt-get upgrade
```

2. Install git `sudo apt-get install git`
3. Copy repo with `git clone https://github.com/Ruczak/satech-cansat22.git`
4. Make sure you have python3 installed `sudo python3`
5. Install package installer for python (PIP) `sudo apt-get install python-pip`
6. Install required dependencies `sudo apt-get install python-smbus python-serial`
7. Install required python libraries `sudo python3 -m pip install RPi.GPIO csv`
8. Open **Serial Port** and **I<sup>2</sup>C Port** with
   1. Type in terminal `sudo raspi-config`
   2. Select **Interface Options**
   3. Select **Serial Port**
   4. Select **No** when asked _Would you like a login shell to be accessible over serial?_
   5. Select **Yes** when asked _Would you like the serial port hardware to be enabled?_
   6. Select **Ok**
   7. Select **Interface Options** again
   8. Select **I2C**
   9. Select **Yes** when asked _Would you like the ARM I2C interface to be enabled?_
   10. Select **Ok**
   11. Select **Finish**
9. Edit config file with:
   1. Type in terminal `sudo nano /boot/config.txt`
   2. Uncomment (delete # sign) or add this line `dtparam=i2c_arm=on`
   3. Add this line `dtoverlay=i2c-gpio,bus=2,i2c_gpio_sda=27,i2c_gpio_scl=22`
10. Reboot with `sudo reboot`
