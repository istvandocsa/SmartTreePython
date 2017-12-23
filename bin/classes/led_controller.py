from threading import Thread
from neopixel import *
from patterns import *

import math


class LedController:
    def __init__(self, queue):
        self.queue = queue

        self.looper = Thread(target=self.process)
        self.looper.daemon = True

        self.pattern_runner = Thread(target=self.run_pattern)
        self.pattern_runner.daemon = True

        self.stats = {
            'last_pattern': tricolor,
            'active_pattern': tricolor,
            'preferred_brightness': 80,
            'preferred_color': Color(0, 255, 0),  # Red
            'pattern_running': True
        }

        self.strip = Adafruit_NeoPixel(145, 18)
        self.strip.begin()

    def run(self):
        self.pattern_runner.start()
        self.looper.start()
        self.strip.setBrightness(self.stats['preferred_brightness'])

    def process(self):
        while True:
            needs_restart = self.get_pattern(self.queue.get(True))
            if needs_restart:
                self.stats['pattern_running'] = False
                while not self.stats['pattern_running']:
                    time.sleep(0.2)

    def run_pattern(self):
        while True:
            self.stats['active_pattern'](self.strip, self.stats)
            self.stats['pattern_running'] = True

    def get_pattern(self, message):
        return {
            'power': self.handle_power,
            'color': self.handle_color,
            'brightness': self.handle_brightness,
            'pattern': self.handle_pattern
        }[message.topic](message.payload)

    def handle_power(self, state):
        print "handle_power payload: " + state
        if "ON" == state:
            self.strip.setBrightness(self.stats['preferred_brightness'])
            self.stats['active_pattern'] = self.stats['last_pattern']

        else:
            self.stats['last_pattern'] = self.stats['active_pattern']
            self.stats['active_pattern'] = no_pattern
        return True

    def handle_color(self, color_rgb):
        r, g, b = color_rgb.split("_")
        print "handle_color payload: RGB(" + r + "," + g + "," + b + ")"
        self.stats['preferred_color'] = Color(int(g), int(r), int(b))
        self.stats['active_pattern'] = static_lights
        return True

    def handle_pattern(self, pattern):
        patterns = {
            'static': static_lights,
            'breathing': breathing,
            'flag': tricolor,
            'swipe': swipe,
            'random swipe': random_swipe,
            'rainbow': rainbow,
            'rainbow cycle': rainbow_cycle,
            'racing': theaterChase

        }
        print "handle_pattern payload:" + pattern
        self.stats['last_pattern'] = self.stats['active_pattern']
        self.stats['active_pattern'] = patterns.get(pattern, static_lights)
        return True

    def handle_brightness(self, brightness_percent):
        print "handle_brightness payload: " + brightness_percent + "%"
        brightness = int(math.floor(2.55 * float(brightness_percent) * 0.3))
        self.stats['preferred_brightness'] = brightness
        self.strip.setBrightness(brightness)
        return False

    def wipe(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
