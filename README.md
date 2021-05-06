# SegaController
Add support of Sega Mega Drive controller to Linux PC

## Controller pinout

![image_1](https://raw.githubusercontent.com/lxxxxl/SegaController/master/img/pinout.png?raw=true)

__Pin  Button (SEL=5V)__  
__D0__   D-pad up  
__D1__   D-pad down  
__D2__   D-pad left  
__D3__   D-pad right  
__D4__   B button  
__D5__   C button  
 
---------------  
__Pin  Button (SEL=0V)__  
__D0__   up  
__D1__   down  
__D2__   GND  
__D3__   GND  
__D4__   A button  
__D5__   Start button  

---------------  
  
__Pin  Button (SEL=5V after 3rd pulse)__  
__D0__   Z button  
__D1__   Y button  
__D2__   X button  
__D3__   Mode button  

## Usage
1. Flash your Arduino board with `SegaController.ino` sketch  
2. Connect Sega Mega Drive controller to Arduino pins this way:
```C++
PIN_UP_OR_Z         -> 6
PIN_DOWN_OR_Y       -> 7
PIN_LEFT_OR_X       -> 8
PIN_RIGHT_OR_MODE   -> 9
PIN_B_OR_A          -> 10
PIN_SEL             -> 11
PIN_C_OR_START      -> 12
```
3. Update `config.json` according to your setup. Set Arduino Serial port, port speed and sleep on error timer:
```json
{
    "device" : "/dev/ttyUSB0",
    "speed" : 9600,
    "sleep" : 30
}
```
4. Setup autostart for `KeyProcessor.py` or run it manually when needed.  
  
## Useful links
[https://eax.me/arduino-sega-controller/](https://eax.me/arduino-sega-controller/)  
[http://www.msarnoff.org/gen2usb/](http://www.msarnoff.org/gen2usb/)
