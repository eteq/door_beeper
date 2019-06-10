# door_beeper
ESP32-based refrigerator/freezer open alarm

Materials:

* Adafruit HUZZAH32 (although really any ESP32 board should work) w/ [Micropython](https://micropython.org).
* Piezo buzzer - e.g. [This one from adafruit](https://www.adafruit.com/product/160)
* 2x contact switches - e.g. [These from adafruit](https://www.adafruit.com/product/375)
* (optional) SONOS speakers

As designed, the piezo goes across GPIO pins 12/33, which are the 5th/7th pin down from "BAT".  The fridge/freezer switches connect GND to 23/21 (respectively).  The switches are open when the door is open, and closed when the door is closed.
