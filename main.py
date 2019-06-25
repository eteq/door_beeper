import uos
import utime
import machine
from machine import Pin, PWM

import utils

default_config = dict(
    sleep_time_ms = 250,
    freezer_delay_ms = 1000,
    fridge_delay_ms = 1000,
    write_battery_voltage = True,
    piezo_plus_pin_num = 12,
    piezo_min_pin_num = 33,
    freezer_switch_pin_num = 23,
    fridge_switch_pin_num = 21
    )
try:
    config_dct = {}
    execfile('config.py', config_dct)
except Exception as e:
    print("Could not run config file, using defaults:", default_config, '. File error:')
    print(e)
    globals().update(default_config)
else:
    for varnm in default_config.keys():
        if varnm in config_dct:
            globals()[varnm] = config_dct[varnm]
            print('Loaded config value for', varnm, ':', config_dct[varnm])
        else:
            globals()[varnm] = default_config[varnm]
            print('Using default config value for', varnm, ':', default_config[varnm])

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

# how often to write out the battery status.  None means don't do it at all
battery_time_spacing_secs = 600

# use an infinite loop to watch for door opening

def check_open(pin, name, open_times_dct, piezo_args, delay_for_alarm_ms):
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

last_battery_time = None
open_times = {'Freezer': None, 'Fridge': None}
while True:
    check_open(freezer_switch_pin, 'Freezer', open_times, ([1300,1000], 10, 500), freezer_delay_ms)
    check_open(fridge_switch_pin, 'Fridge', open_times, ([1200,900], 10, 500), fridge_delay_ms)
    utime.sleep_ms(sleep_time_ms)

    # write out battery status if desired
    if battery_time_spacing_secs is not None:
        if last_battery_time is None:
            last_battery_time = utime.time()
        else:
            if (utime.time() - last_battery_time) > battery_time_spacing_secs:
                voltage = utils.read_battery_voltage()
                print('Battery level:', voltage, 'V')
                if write_battery_voltage:
                    with open('battery_voltage', 'a') as f:
                        f.write(str(utime.time()))
                        f.write(' ')
                        f.write(str(voltage))
                        f.write('\n')
                last_battery_time = utime.time()
