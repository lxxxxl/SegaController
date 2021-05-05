import os
import serial
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

def process(key):
    if not key in keyassoc:
        return
    keyevent = keyassoc[key]

    os.system("xdotool key " + keyevent)


def main():
    with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
        while True:
            x = ser.read()
            if len(x) != 1:
                continue
            if not Keys.has_value(x[0]):
                continue

            process(Keys(x[0]))

main()