import pixy2
import json
from time import sleep

device = pixy2.Pixy2I2C()

# set a mode
device.set_mode(pixy2.LINE_MODE_WHITE_LINE)

# get version from pixy2
hw, sw = device.get_version()
string = 'hw {} sw {}'.format(hw, sw)
print(string)
#
# get resolution from pixy2
resolution = device.get_resolution()
string = 'width {} height {}'.format(*resolution)
print(string)
#
# set brightness for pixy2
for brightness in range(0, 150, 30):
    device.set_camera_brightness(brightness)
    sleep(0.5)

# set servos pans
for pan in range(0, 512, 128):
    tilt = pan
    device.set_servos(pan, tilt)
    sleep(0.3)

# set the RGB LED
for color_channel in range(0, 256 + 1, 64):
    r = g = b = color_channel
    device.set_led(r, g, b)
    sleep(0.1)

# turn the lamp on an off
counter = 0
for i in range(10):
    device.set_lamp(counter % 2)
    counter += 1
    sleep(0.05)

# get FPS
fps = device.get_fps()
print('pixy2\'s camera FPS is {}'.format(fps))

# get blocks
retries = 10
counter = 0
while True:
    block = device.get_blocks(sigmap=255, maxblocks=255)
    sleep(0.1)
    counter += 1
    if block is not None:
        break
    if counter == retries:
        break
if counter != retries:
    string = 'sign={} XC={} YC={} W={} H={} Angle={} Idx={} Age={}'.format(*block)
    print(string)

# get main features
retries = 10
counter = 0
device.set_lamp(1)
while True:
    features = device.get_main_features(features=1)
    sleep(0.1)
    counter += 1
    if features is not None:
        break
    if counter == retries:
        break

if counter != retries:
    formatted = json.dumps(features, indent=2, sort_keys=True)
    print(formatted)

# set the next turn's angle
device.set_next_turn(0)

# set the default turn angle
device.set_default_turn(0)

# select the vector to track
device.set_vector(0)

# double reverse the vectors
device.reverse_vector()
device.reverse_vector()

# turn the lamp off
device.set_lamp(0)
