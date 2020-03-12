# Copyleft (c) 2020 HandsomeYingyan@gmail.com
# A simple PY to test basic car function
# Release Under GPLv3 Licence

import os
import time
import gpio3
import re
import sys
import tty
import termios


sunxi_gpio_lay = re.compile(r"P([A-Z])(\d+)")


'''sunxi layout'''
a_bool=False
b_bool=False
c_bool=False
d_bool=False

exit_bool=True

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

def is_sunxi(pin):
    ma = sunxi_gpio_lay.fullmatch(pin)
    if ma is None:
        return False
    else:
        return True

def listen(key): 
    if key == 'w':
        print('Up start')
        in1.value = 1
        in2.value = 0
        in3.value = 1
        in4.value = 0
        clean_gpio()

    elif key == 's':
        print("down start")
        in1.value = 0
        in2.value = 1
        in3.value = 0
        in4.value = 1
        clean_gpio()

    elif key == 'a':
        print("left start")
        in1.value = 1
        in2.value = 0
        in3.value = 0
        in4.value = 1
        clean_gpio()

    elif key == 'd':
        in1.value = 0
        in2.value = 1
        in3.value = 1
        in4.value = 0
        print("right start")
        clean_gpio()

    elif key == 'q':
        return False

    return True



def print_banner(): #logo
    print("***************************************")
    print("****      Handsome Car Tester      ****")
    print("***************************************")
    print("--W to Forward,S to back,A to Right,D to Left")
    print("In1: " + a + " IN2:" + b +" IN3:"+ c +" IN4:"+ d)

def set_gpio(a,b,c,d): #set up gpios
    in1.direction = "out"
    in2.direction = "out"
    in3.direction = "out"
    in4.direction = "out"

def clean_gpio():  #remove all the motion
    in1.value=0
    in2.value=0
    in3.value=0
    in4.value=0

print("Handsome Car Tester")
print("Test Basic Function On you Allwinner-based(sunxi) Car")
print("Warning: Only Working in mainline kernel!!!(sysfs)")
print("Requirement:  gpio3")
print("Now Setting Gpios(Input Sunxi-style Gpios):")

while not a_bool:
    a=input("What is connect to IN1 pin:")
    a_bool=is_sunxi(a)
    if not a_bool:
        print("Invaild Gpio Format!")
        continue


while not b_bool:
    b=input("What is connect to IN2 pin:")
    b_bool=is_sunxi(b)
    if not b_bool:
        print("Invaild Gpio Format!")
        continue


while not c_bool:
    c=input("What is connect to IN3 pin:")
    c_bool=is_sunxi(c)
    if not c_bool:
        print("Invaild Gpio Format!")
        continue


while not d_bool:
    d=input("What is connect to IN4 pin:")
    d_bool=is_sunxi(d)
    if not d_bool:
        print("Invaild Gpio Format!")
        continue

in1=gpio3.LinuxGPIO(gpio3.mainline_sunxi_pin(a))
in2=gpio3.LinuxGPIO(gpio3.mainline_sunxi_pin(b))
in3=gpio3.LinuxGPIO(gpio3.mainline_sunxi_pin(c))
in4=gpio3.LinuxGPIO(gpio3.mainline_sunxi_pin(d))
set_gpio(a,b,c,d)


os.system("clear")
print_banner()

while exit_bool:
    exit_bool=listen(readkey())


print("Thanks! Hope Your Project Can Work Normally!")
