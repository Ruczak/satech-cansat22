# Sesnor Wiring for Cansat:
## Raspberry Pi Zero 2 W - Header Pinout

<img src="https://i.stack.imgur.com/yHddo.png" height="450px" alt="header pinout" />

## I<sup>2</sup>C Busses:
### I2C_1 (default)
- Vdd: 1 (3.3V)
- GND: 6
- SCL: 5 (GPIO3)
- SDA: 3 (GPIO2)

### I2C_2 (custom)
- Vdd: 17 (3.3V)
- GND: 20
- SCL: 13 (GPIO27)
- SDA: 11 (GPIO17)

## Sensors
### BMP280 Bosch:
- Bus: I2C_1
- Address: 0x76
- Voltage: 3.3V

### MCP9808 Adafruit:
- Bus: I2C_2
- Address: 0x18
- Voltage: 3.3V
