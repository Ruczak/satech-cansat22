# SaTech Team CanSat

### Edition 2021/22

<img src="https://drive.google.com/uc?export=view&id=1Y8iNRtcaDI3GDSQ605UacmiUN2jqexMc" style="height: 300px; max-height: 100%; width: auto" />

## Introduction

This is source code of a **SaTech's CanSat**.

To see how are sensors, buzzer and LED wired, go to SENSOR_WIRING.md

## Installation

1. Check for updates

```
sudo apt-get update
sudo apt-get upgrade
```
2. Make sure you have python3 (version 3.9 or higher) installed `sudo python3 --version` if not install it.
3. Install git and required dependencies `sudo apt-get install git python-smbus python-serial gpsd gpsd-clients libusb-1.0-0-dev cmake`
4. Copy repo with `git clone https://github.com/Ruczak/satech-cansat22.git`
5. Install required python libraries `sudo python3 -m pip install RPi.GPIO bmp280 gps smbus2 Adafruit_MCP9808 pyrtlsdr`
6. Open **Serial Port** and **I<sup>2</sup>C Port** with
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
7. Edit config file with `sudo nano /boot/config.txt` and add or uncomment
```
dtparam=i2c_arm=on
dtparam=i2c_vc=on
```
10. Install librtlsdr with
```
git clone git://git.osmocom.org/rtl-sdr.git
cd rtl-sdr
mkdir build
cd build
cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON
make
sudo make install
sudo ldconfig
cd ~
sudo cp ./rtl-sdr/rtl-sdr.rules /etc/udev/rules.d/
```
11. Modify GPS' config file with `sudo nano /etc/default/gpsd` and add these lines
```
START_DAEMON="true"
USBAUTO="true"
DEVICES="/dev/ttyUSB0"
GPSD_OPTIONS="-F /var/run/gpsd.sock"
```
12. Run GPS socket with `sudo systemctl enable gpsd.socket` and `sudo systemctl start gpsd.socket`
13. Add permissions to start script with `chmod +x ./start.sh`
14. Reboot with `sudo reboot`
15. Run `sudo ./start.sh`
