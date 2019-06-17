import math
import utime
import usocket
from machine import Pin, ADC, RTC

# https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/adc.html says 0 dB is 1.1 V
ADC_to_voltage = lambda adc, attendb=0: 1.1*10**(attendb/20)*adc.read()/4095

def read_battery_voltage(pin=35):
    adc = ADC(Pin(pin))
    adc.atten(ADC.ATTN_11DB)
    return 2*ADC_to_voltage(adc, 11)

def piezo_multitone(pwm, freqs, n_waves, timeout_ms):
    if timeout_ms is None:
        timeout_ms = float('inf')

    minfreq = min(freqs)
    sleep_ms = math.ceil(n_waves*1000/minfreq)

    pwm.freq(freqs[0])
    pwm.init()
    start = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), start) < timeout_ms:
        for f in freqs:
            pwm.freq(f)
            utime.sleep_ms(sleep_ms)
    pwm.deinit()


def set_time_from_nist(assume_day=0, init_rtc=True):
    addr = usocket.getaddrinfo('time.nist.gov', 13)[0][-1]
    s = socket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s.connect(addr)
    result = s.recv(1024)
    s.close()

    yr, mo, day = result[7:15].split(b'-')
    hr, mn, sec = result[16:24].split(b':')
    tt = (int(yr)+2000, int(mo), int(day), assume_day, int(hr), int(mn), int(sec), 0)

    if init_rtc:
        RTC().init(tt)

    return tt
