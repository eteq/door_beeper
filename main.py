import utime
import machine
from machine import Pin, PWM

import utils


piezo_plus_pin_num = 12
piezo_min_pin_num = 33

freezer_switch_pin_num = 21
fridge_switch_pin_num = 23

# setup pins
led_pin = Pin(13, Pin.OUT)
piezo_min_pin = Pin(piezo_min_pin_num, Pin.OUT)

freezer_switch_pin = Pin(freezer_switch_pin_num, Pin.IN, Pin.PULL_UP)
fridge_switch_pin = Pin(fridge_switch_pin_num, Pin.IN, Pin.PULL_UP)

#set initial state of pins
piezo_min_pin.value(0)
led_pin.value(0)

# set up PWM
piezo_plus_pwm = PWM(Pin(piezo_plus_pin_num), duty=512)
piezo_plus_pwm.deinit()

# use an infinite loop to watch for door opening

def check_open(pin, name, open_times_dct, piezo_args):
    led_pin.value(0)
    if pin.value() == 1:
        print(name, 'open...')
        led_pin.value(1)
        if open_times[name] is None:
           open_times[name] = utime.ticks_ms()
        else:
            dt = utime.ticks_diff(utime.ticks_ms(), open_times[name])
            if dt > delay_for_alarm_ms:
                print(name, 'has been open for more than', delay_for_alarm_ms, 'ms!')
                utils.piezo_multitone(piezo_plus_pwm, *piezo_args)
    else:
        if open_times[name] is not None:
            print(name, 'closed.')
        open_times[name] = None

sleep_time_ms = 250
delay_for_alarm_ms = 1000

open_times = {'Freezer': None, 'Fridge': None}
while True:
    check_open(freezer_switch_pin, 'Freezer', open_times, ([1300,1000], 10, 500))
    check_open(fridge_switch_pin, 'Fridge', open_times, ([1200,900], 10, 500))
    utime.sleep_ms(sleep_time_ms)
