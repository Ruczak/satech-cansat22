sudo stty -F /dev/ttyUSB0 9600
echo "Set baud rate of /dev/ttyUSB0 to 9600"
echo "================"
echo "STARTING PROGRAM"
sudo python3 ./main.py
