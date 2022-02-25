# Wiring for CanSat:

## Raspberry Pi Zero 2 W - Header Pinout

<img src="https://i.stack.imgur.com/yHddo.png" height="450px" alt="header pinout" />

## I<sup>2</sup>C buses:

### I2C_1

- Vdd: 1 (3.3V)
- GND: 6
- SCL: 5 (GPIO3)
- SDA: 3 (GPIO2)

### I2C_0

- Vdd: 17 (3.3V)
- GND: 30
- SCL: 28 (ID_SC)
- SDA: 27 (ID_SD)

## Sensors

### BMP280 Bosch

- Bus: I2C_1
- Address: 0x76
- Voltage: 3.3V

### MCP9808 Adafruit

- Bus: I2C_0
- Address: 0x18
- Voltage: 3.3V

## Buzzer and LED wiring:

### Passive buzzer

- Red (PWR): 40 (GPIO21)
- Black (GND): 34

### LED

- Cathode (+ / PWR): 37 (GPIO26)
- Anode (- / GND): 39