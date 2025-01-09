import adafruit_ssd1306 as ssd1306
import board
import busio
import digitalio as GPIO
import time
from math import pi, cos, sin

#SCREEN SETUP
i2c = busio.I2C(board.SCL, board.SDA)       # Define I2C-Port (might need adjustment for different screens)
xres=64 #Resolution of X-Axys
yres=48 #Resolution of Y-Axys
oled = ssd1306.SSD1306_I2C(xres, yres, i2c)

#BOARD SETUP
pwm = GPIO.DigitalInOut(board.A1)
switch = GPIO.DigitalInOut(board.A0)
pwm.pull = GPIO.Pull.UP
switch.pull = GPIO.Pull.UP
counter = 0

#PWM-RANGE SETUP (REQUIRED)
pwm_min = 950 # USE DEBUG MENU TO SET THIS
pwm_max = 1953 # USE DEBUG MENU TO SET THIS

pwm_diff = pwm_max-pwm_min

def startup():
    '''
    Simple startup screen with Text on screen
    '''
    oled.fill(0)
    oled.text("S.J.",22,25,1)
    oled.show()
    time.sleep(0.5)

def pwm_pulse(pin, timeout_ns=1000000000):
    """
    Measures the time difference of a PWM signal transition from 0 to 1 to 0.

    Parameters:
        pin: Input to pull data from
        timeout_ns (int): Time based value in nanoseconds to prevent hanging (default is 1 second).

    Returns:
        int: Time difference in nanoseconds representing the pulse width.
        bool: Value 0 if Timeout-citeria is fulfilled
    """
    # Wait for the signal to change to 1
    timeout = time.monotonic_ns() + timeout_ns
    while pin.value == 0:
        if time.monotonic_ns() > timeout:
            return 0

    # Record the start time when the signal changes to 1
    start_time = time.monotonic_ns()

    # Wait for the signal to change back to 0
    timeout = time.monotonic_ns() + timeout_ns
    while pin.value == 1:
        if time.monotonic_ns() > timeout:
            return 0

    # Calculate and return the time difference
    pulse_width = time.monotonic_ns() - start_time
    return pulse_width

def pwm_percentage(time_ns, pwm_min, pwm_diff):
    """
    Calculate percentage of PWM input

    Parameters:
        time_ns (float): Time in Nanoseconds.
        pwm_min (float): Minimum PWM value.
        pwm_diff (float): Difference between max and min PWM values.

    Returns:
        float: The calculated PWM value as a percentage.
    """
    if time_ns == 0:
        return time_ns
    else:
        # Normalize the time and calculate the percentage, clamping to Range
        normalized_value = (time_ns / 1000) - pwm_min
        percentage = round((normalized_value / pwm_diff) * 100, 3)
        percentage_clamped = max(0, min(100, percentage))
    return percentage_clamped

def draw_circle(xpos0, ypos0, radius, color=1):
    """
    Draws a circle using the Midpoint Circle Algorithm.

    Parameters:
        xpos0 (int): X-coordinate of the circle's center.
        ypos0 (int): Y-coordinate of the circle's center.
        radius (int): Radius of the circle.
        color (int): Color to draw the circle with:
                        1 = white (pixel is on)
                        0 = black (pixel is off)
    Returns:
        None: Directly draws on the screen.
    """
    x = radius - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (radius << 1)
    while x >= y:
        # Draw the circle
        oled.pixel(xpos0 + x, ypos0 + y, color)
        oled.pixel(xpos0 + y, ypos0 + x, color)
        oled.pixel(xpos0 - y, ypos0 + x, color)
        oled.pixel(xpos0 - x, ypos0 + y, color)
        oled.pixel(xpos0 - x, ypos0 - y, color)
        oled.pixel(xpos0 - y, ypos0 - x, color)
        oled.pixel(xpos0 + y, ypos0 - x, color)
        oled.pixel(xpos0 + x, ypos0 - y, color)
        # Update error and step values
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (radius << 1)

def draw_speedometer(xpos0, ypos0, radius, percentage, circle=1): 
    """
    Draws a speedometer with a pointer that adjusts based on a percentage-value.

    Parameters:
        xpos0 (int): X-coordinate of the speedometer's center.
        ypos0 (int): Y-coordinate of the speedometer's center.
        radius (int): Radius of the speedometer.
        pointer_pos (int): Pointer position as a percentage (0 to 100).

    Returns:
        None: Directly draws on the screen.
    """
    # Clamping pointer position between 0 and 100 (prevents an out-of-bounds pointer)
    pointer_pos = max(0, min(100, percentage))
    
    # Calculate the angle in radians (starts at 180° and decreases clockwise)
    angle = pi - (pi * (pointer_pos / 100))

    # Draw the pointer line from the center to the edge of the semicircle (endpoint calculation)
    for i in range(0, int(radius), 1):
        x_end = int(xpos0 + i * cos(angle))
        y_end = int(ypos0 - i * sin(angle))
        oled.pixel(x_end, y_end, 1)

    # Draw the semicircular outline
    x = radius - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (radius << 1)

    while x >= y:
        # Draw only the upper half of the circle
        oled.pixel(xpos0 + x, ypos0 - y, 1)  # Top right
        oled.pixel(xpos0 + y, ypos0 - x, 1)  # Top right
        oled.pixel(xpos0 - y, ypos0 - x, 1)  # Top left
        oled.pixel(xpos0 - x, ypos0 - y, 1)  # Top left

        # Update error and step values
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (radius << 1)

    # Optional: Draw the full circle outline for improved looks
    if circle == 1:       
        draw_circle(xpos0, ypos0, radius+5, color=1)

def pwm_debug_menu():
    '''
    Debug Menu used for PWM-readout or initial setup
    '''
    # Shows direct PWM-Values. This can be used to initially set pwm_min and pwm_max.
    oled.fill(0)
    oled.text(f"{int(pwm_pulse(pin=pwm)/1000)}",20, 15, 1)
    oled.text("debug", 18,25,1)
    oled.show()

try:
    startup()
    while 1:
        # Main Screen
        while switch.value == 0:
            pulse = pwm_pulse(pin=pwm)
            percentage = pwm_percentage(pulse, pwm_min, pwm_diff)
            counter += 1
            if counter >= 3:
                oled.fill(0)
                draw_speedometer(32, 25, 17, percentage)
                #Write percentage as Text below speedometer
                if percentage == 100:
                    oled.text(f"{int(percentage)}",24, 30, 1)
                elif percentage >= 10:
                    oled.text(f"{int(percentage)}",27, 30, 1)
                else:
                    oled.text(f"{int(percentage)}",31, 30, 1)
                oled.show()
                counter = 0
            if switch.value ==1:
                break
        # Debug Menu
        while switch.value == 1:
            pwm_debug_menu()
            if switch.value ==0:
                break
except Exception as err:
    print(Exception, err)
    print("Error")
    oled.fill(0)
    oled.text("Error",18,25,1)
    oled.show()