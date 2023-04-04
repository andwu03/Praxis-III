
'''
ESC204 2023S 
'''
# PROCESS
# PUT SLIDE INTO BOX
# Listen for button press, wait A seconds before starting cycle
# Note: Second button press before end of cycle will cancel cycle
# Turn on LED to indicate that cycle has started
# Turn on fan for B seconds
# Open valve to Giemsa for C seconds
# Sleep for 8-10 minutes
# Open drain valve 
# Open valve to water for D seconds
# Turn on fan until slide is dry again
# Close drain valve (after all fluids have been drained)
# Blink LED (or turn on another LED) to indicate that cycle is complete
# TAKE SLIDE OUT OF BOX
# Listen for button press to restart process

# IMPORTS
import board
import digitalio
import time
import pwmio
from adafruit_motor import servo

# PORTS
red_led_port = board.GP15
green_led_port = board.GP14

pwm_input_port = board.GP16
pwm_output_port = board.GP17

button_port = board.GP12
fan_port = board.GP13

# CONSTANTS
slide_dry_time = 30
giemsa_input_time = 30
staining_time = 10 # 8*60
giemsa_drain_time = 30
water_input_time = 30
water_drain_time = 30
final_dry_time = 30

# CONFIGURE
# RED LED
ledRed = digitalio.DigitalInOut(red_led_port) # red
ledRed.direction = digitalio.Direction.OUTPUT

# GREEN LED
ledGreen = digitalio.DigitalInOut(green_led_port) # red
ledGreen.direction = digitalio.Direction.OUTPUT

# SERVO INPUT
pwm_input = pwmio.PWMOut(pwm_input_port, duty_cycle=2**15, frequency=50)
servo_input = servo.Servo(pwm_input)

# SERVO INPUT
pwm_output = pwmio.PWMOut(pwm_output_port, duty_cycle=2**15, frequency=50)
servo_output = servo.Servo(pwm_output)

# BUTTON
button = digitalio.DigitalInOut(button_port)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Set the internal resistor to pull-up, meaning True and False will be flipped

# FAN
fan = digitalio.DigitalInOut(fan_port) # red
fan.direction = digitalio.Direction.OUTPUT

def if_pressed(buttonvalue):
    if (buttonvalue == False):
        return True
    return False

#--------------------------------------------------#

# Print a message on the serial console
# print('READY')

second_press = False
        
# Loop so the code runs continuosly

while True: 
    ledGreen.value = False
    ledRed.value = False
    # Listen for button press
    while(button.value == True):
        continue

    led_start = time.time()
    # Blink red LED for 5 seconds to indicate that cycle will start soon
    while(time.time() - led_start < 5):
        ledRed.value = True
        time.sleep(0.5)
        ledRed.value = False
        time.sleep(0.5)
    
    # Turn red LED on to indicate that cycle is in progress
    ledRed.value = True
       
    fan1_start = time.time()
    # Turn fan on and off - good
    while (time.time() - fan1_start < slide_dry_time):
        fan.value = True
    fan.value = False

    # Open valve to Giemsa
    # 0 − 180 degrees, 5 degrees at a time.
    print('Rotating to 180')
    for angle in range(0, 180, 5):
        ledGreen.value = True
        servo_input.angle = angle
        time.sleep(0.05)
    ledGreen.value = False

    # Wait to fill compartment
    time.sleep(giemsa_input_time)
    
    # Close valve to Giemsa
    # 180 − 0 degrees, 5 degrees at a time.
    for angle in range(180, 0, -5):
        ledGreen.value = True
        servo_input.angle = angle 
        time.sleep(0.05)
    ledGreen.value = False

    # Stain
    time.sleep(staining_time)

    # Open drain valve
    for angle in range(0, 180, 5):
        ledGreen.value = True
        servo_output.angle = angle
        time.sleep(0.05)
    ledGreen.value = False

    # Open water valve
    for angle in range(0, 180, 5):
        ledGreen.value = True
        servo_input.angle = angle
        time.sleep(0.05)
    ledGreen.value = False

    # Flush
    time.sleep(water_input_time)

    # Close valve to water
    for angle in range(180, 0, -5):
        ledGreen.value = True
        servo_input.angle = angle 
        time.sleep(0.05)
    ledGreen.value = False

    fan2_start = time.time()
    # Turn fan on and off to dry after flushing
    while (time.time() - fan2_start < final_dry_time):
        fan.value = True
    fan.value = False

    # Close drain valve
    for angle in range(180, 0, -5):
        ledGreen.value = True
        servo_output.angle = angle 
        time.sleep(0.05)
    ledGreen.value = False

    time.sleep(5)

    # Turn red LED off and green LED on to indicate that cycle is complete
    ledRed.value = False
    ledGreen.value = True

    # Wait 5 seconds and turn green LED off
    time.sleep(5)
    ledGreen.value = False