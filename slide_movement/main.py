import time

# load the CircuitPython hardware definition module for pin definitions
import board

# load the CircuitPython GPIO support
import digitalio

#--------------------------------------------------------------------------------

#conversion factor for system (in motor steps/mm)
CONV_FACT = 50

class A49881:
    def __init__(self, DIR=board.GP16, STEP=board.GP17):


        self._dir  = digitalio.DigitalInOut(DIR)
        self._step = digitalio.DigitalInOut(STEP)

        self._dir.direction  = digitalio.Direction.OUTPUT
        self._step.direction = digitalio.Direction.OUTPUT

        self._dir.value = False
        self._step.value = False

    def step(self, forward=True):

        self._dir.value = forward

        # Create a short pulse on the step pin.  Note that CircuitPython is slow
        # enough that normal execution delay is sufficient without actually
        # sleeping.
        self._step.value = True
        # time.sleep(1e-6)
        self._step.value = False

    def move_sync(self, steps, speed=10):

        self._dir.value = (steps >= 0)
        time_per_step = 1.0 / speed
        for count in range(abs(steps)):
            self._step.value = True
            # time.sleep(1e-6)
            self._step.value = False
            time.sleep(time_per_step)

    def move_oned (self, distance, bsteps, speed):

        #need to find limit to distance/bsteps (ie minimum step size in distance)
        msteps = CONV_FACT * (distance/bsteps)

        self.move_sync (msteps, speed)



    def deinit(self):

        self._dir.deinit()
        self._step.deinit()
        self._dir  = None
        self._step = None

    def __enter__(self):
        return self

    def __exit__(self):
        # Automatically deinitializes the hardware when exiting a context.
        self.deinit()

#--------------------------------------------------------------------------------
# Stepper motor demonstration.

class A49882:
    def __init__(self, DIR=board.GP18, STEP=board.GP19):


        self._dir  = digitalio.DigitalInOut(DIR)
        self._step = digitalio.DigitalInOut(STEP)

        self._dir.direction  = digitalio.Direction.OUTPUT
        self._step.direction = digitalio.Direction.OUTPUT

        self._dir.value = False
        self._step.value = False

    def step(self, forward=True):

        self._dir.value = forward

        # Create a short pulse on the step pin.  Note that CircuitPython is slow
        # enough that normal execution delay is sufficient without actually
        # sleeping.
        self._step.value = True
        # time.sleep(1e-6)
        self._step.value = False

    def move_sync(self, steps, speed=10):

        self._dir.value = (steps >= 0)
        time_per_step = 1.0 / speed
        for count in range(abs(steps)):
            self._step.value = True
            # time.sleep(1e-6)
            self._step.value = False
            time.sleep(time_per_step)

    def move_oned (self, distance, bsteps, speed):

        #need to find limit to distance/bsteps (ie minimum step size in distance)
        msteps = CONV_FACT * (distance/bsteps)

        self.move_sync (msteps, speed)


    def deinit(self):

        self._dir.deinit()
        self._step.deinit()
        self._dir  = None
        self._step = None

    def __enter__(self):
        return self

    def __exit__(self):
        # Automatically deinitializes the hardware when exiting a context.
        self.deinit()

#--------------------------------------------------------------------------------
# Stepper motor demonstration.


stepperx = A49881()
steppery = A49882()
print("Starting stepper motor test.")

speed = 50
xdistance = 15
ydistance = 15
xbsteps = 4
ybsteps = 4
photo_time = 1
ydir = 1
xdir = 1
prev = 1

button = digitalio.DigitalInOut(board.GP10)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Set the internal resistor to pull-up

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    curr = button.value # Current value of the button


    if prev == 0 and curr == 1:
    # If the last state of the button was "down"
    # and the current state of the button is "up,"
    # the button was pushed -> Go to the next mode
        led.value = True

        for y in range (ybsteps-1):

            time.sleep (photo_time) #photo1


            for x in range (xbsteps-1):
                #takes photo 2 to end
                stepperx.move_oned (xdir*xdistance, xbsteps, speed)
                time.sleep(photo_time)

            xdir = -1*xdir
            steppery.move_oned (ydir*ydistance, ybsteps, speed)

        ydir = -1*ydir

    prev = curr
    led.value = False

    time.sleep(0.1)
