# SimplePWMDash
A simple PWM signal-based dashboard for RC boats, cars, and planes using the Adafruit QT Py RP2040, a RaspberryPi based microcontroller.

![PXL_20250109_095446982 RAW-01 COVER](https://github.com/user-attachments/assets/45aaeabc-277c-4c32-9255-9a5fbc4fc14c)

## Features

- Dashboard view: PWM Signal as a speedometer-like graphic.
- Debug view: Current PWM Status for debug or setup

## Hardware
- Adafruit QT Py RP2040 (https://www.adafruit.com/product/4900)
- OLED Display 0.66" (https://wiki.seeedstudio.com/Grove-OLED-Display-0.66-SSD1306_v1.0/)
- 10kΩ Resisitor
- Positional Switch
- Optional: PWM Servo-Tester (for generating PWM-Signal)

## Software
- Thonny 4.1.6 or newer (for easy interfacing with QT Py RP2040), not required (https://thonny.org/)
- CircuitPython 9.2.1 or newer (https://circuitpython.org/board/adafruit_qtpy_rp2040/)

## Requirements

1. CircuitPython <br />
  This Project requires CircuitPython 9.2.1 or newer installed on your Adafruit QT Py RP2040.
  A guide on this can be found here:
  https://learn.adafruit.com/adafruit-qt-py-2040/circuitpython

2. Dependencies <br />
  To run this on your QT Py you need the following modules. <br />
  - Adafruit-SSD1306 2.12.18 or newer (https://github.com/adafruit/Adafruit_CircuitPython_SSD1306)
  - Adafruit-framebuf 1.6.6 or newer (https://github.com/adafruit/Adafruit_CircuitPython_framebuf)

## Installation

1. Install all Requirements <br />
   Follow this Guide for Circuit Python installation: https://learn.adafruit.com/adafruit-qt-py-2040/circuitpython <br />
   For dependencies, simply place the .py files in the /lib/ folder on your QT Py so it looks like this:

   ![image](https://github.com/user-attachments/assets/937a033d-f6ae-4b80-a59e-201b58059108)

2. Wiring up the QT Py<br />
   If you're using the exact components listet above, follow the diagram below.
   I take no responsability for any hardware-damage, please check the wiring diagrams by the manufacturer first. <br />
   
   ![image](https://github.com/user-attachments/assets/6f13b2b7-046b-4242-8da4-30eaa3c9c9bf)
   

5. Copying the Dashboard to QT Py<br />
   Download this Repository and copy dash.py directly to the root folder of your QT Py.
   (Once you plug in your QT Py it should appear as an external drive. Please ensure you installed Circuit Python before doing this.)<br />

   If you want your QT Py to start the dash automatically after booting, to the following:
   - Rename the File "dash.py" to "code.py".
   - Reboot

6. Adjusting Settings in dash.py <br />

   Screen and Pin setup:
   If you use the same setup as above, you do not need to change anything.
   If not, please adjust as needed. Please check the manual of your hardware.
   
   Setting up min and max:
   Connect a PWM-source and switch to the debug menu.
   From there take note of the minimum and maximum value shown.
   Enter your values in dash.py.
   Save and reboot.

## Usage

If everything is done correctly, your QT Py should now boot once connected to a Transmitter. If you are using a Servo-Tester, you most likely have to power it via USB C.
If needed you access the debug menu at any time using the connected switch.

Further commands are not needed, Dash is designed to run on its own.
Now you can use your dash.


## Contributing

Guidelines for contributing to the project:

  1. Fork the repository.
  2. Create a new branch for your feature or bugfix:

  ```bash
  git checkout -b feature-name
  ```
  
  3. Commit your changes:
  
  ```bash
  git commit -m "Add feature-name"
  ```
  
  4. Push the branch:
  
  ```bash
  git push origin feature-name
  ```
  
  5. Open a pull request.

## Acknowledgments

This project was created in connection with the FHGR Computer Science module.

Inspiration on how to read PWM with RaspberryPi / Python:
https://www.youtube.com/watch?v=bxdPWrEhbto&ab_channel=CustomRaspi

