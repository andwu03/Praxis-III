'''
ESC204 2023S Lab 2 Task C
Task: Blink an external LED.
'''
# Import libraries needed for blinking the LED
import board
import digitalio
import time

#PORTS
button_port = board.GP1
fan_port = board.GP2
giemsa_valve_port = board.GP3
water_valve_port = board.GP4
alcohol_valve_port = board.GP5
drain_port = board.GP6

slide_dry_time = 30
giemsa_input_time = 30
giemsa_drain_time = 30
water_input_time = 30
water_drain_time = 30
final_dry_time = 30












# Configure the internal GPIO connected to the LED as a digital output
led1 = digitalio.DigitalInOut(board.GP4) # blue
led1.direction = digitalio.Direction.OUTPUT

led2 = digitalio.DigitalInOut(board.GP26) # red
led2.direction = digitalio.Direction.OUTPUT

led3 = digitalio.DigitalInOut(board.GP27) # green
led3.direction = digitalio.Direction.OUTPUT

# Configure the internal GPIO connected to the button as a digital input
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Set the internal resistor to pull-up, meaning True and False will be flipped

# Print a message on the serial console
print('Hello! My LED is blinking now.')

state = 2
timer = 0
led1.value = False
led2.value = False
led3.value = False

# Loop so the code runs continuously
while True:
    if (button.value == False):
        start = time.time()
        while (button.value == False):
            timer = time.time() - start # time elapsed
            if (timer >= 2):
                state = 2
                timer = 0
                break
            elif (button.value == True):
                timer = 0
                state = (state + 1)%2
                break
            
        print(state)
        
        if (state == 0): # for plants
            led1.value = True
            led2.value = True
            led3.value = False
        elif (state == 1): # for humans
            led1.value = True
            led2.value = True
            led3.value = True
        elif (state == 2): # for off
            led1.value = False
            led2.value = False
            led3.value = False
            time.sleep(2)