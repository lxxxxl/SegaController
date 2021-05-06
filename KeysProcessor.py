import os
import serial
import json
import time
from enum import Enum
# enum of keys on Sega controller
class Keys(Enum):
    KEY_UP      = 0
    KEY_DOWN    = 1
    KEY_LEFT    = 2
    KEY_RIGHT   = 3

    KEY_START   = 4
    KEY_MODE    = 5

    KEY_A       = 6
    KEY_B       = 7
    KEY_C       = 8

    KEY_X       = 9
    KEY_Y       = 10
    KEY_Z       = 11
    KEY_MAX     = 12

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

# association of Sega key to keyboard key
keyassoc = {
    Keys.KEY_UP:    'Up',
    Keys.KEY_DOWN:  'Down',
    Keys.KEY_LEFT:  'Left',
    Keys.KEY_RIGHT: 'Right',
    Keys.KEY_START: 'Return',
    Keys.KEY_MODE:  'BackSpace',
    Keys.KEY_A:     'z',
    Keys.KEY_B:     'x',
    Keys.KEY_C:     'c',
    Keys.KEY_X:     'a',
    Keys.KEY_Y:     's',
    Keys.KEY_Z:     'd'
}

def keydown(key):
    if not key in keyassoc:
        return
    keyevent = keyassoc[key]
    os.system("xdotool keydown " + keyevent)

def keyup(key):
    if not key in keyassoc:
        return
    keyevent = keyassoc[key]
    os.system("xdotool keyup " + keyevent)

def loop(device, speed):
    with serial.Serial(device, speed) as ser:
        while True:
            x = ser.read()
            # key code stored in first 4 bits
            key = x[0] & 0x0F
            # key press status stored in 7nth bit (1 - pressed, 0 - released)
            keypressed = x[0] & 0x80
            if not Keys.has_value(key):
                continue
            if keypressed:
                keydown(Keys(key))
            else:
                keyup(Keys(key))

def main():
    # read config file
    path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isfile(path + '/config.json'):
        print('config.json not found')
        exit(1)
    with open(path + '/config.json', 'r') as read_file:
                config = json.load(read_file)

    # try to communicate with serial
    while True:
        # wait while device appears
        if not os.path.exists(config['device']):
            time.sleep(config['sleep'])
        else:
            try:
                # connect to device
                print('connecting to %s' % config['device'])
                loop(config['device'], config['speed'])
            except:
                # device disconnect occured
                print('device disconnected')
                pass


    

main()