import utime
import machine
from machine import Pin, PWM

import utils


piezo_plus_pin_num = 12
piezo_min_pin_num = 33

# setup pins
led_pin = Pin(13, Pin.OUT)
piezo_min_pin = Pin(piezo_min_pin_num, Pin.OUT)

#set initial state of pins
piezo_min_pin.value(0)
led_pin.value(0)

# set up PWM
piezo_plus_pwm = PWM(Pin(piezo_plus_pin_num), duty=512, freq=1000)

utils.piezo_multitone(piezo_plus_pwm, [1300,1000], 25, 1000)