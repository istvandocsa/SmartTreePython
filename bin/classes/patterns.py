import random
import math
import time
from neopixel import Color


def static_lights(strip, stats):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, stats['preferred_color'])
    strip.show()
    while stats['pattern_running']:
        time.sleep(0.2)


def no_pattern(strip, stats):
    strip.setBrightness(0)
    strip.show()
    while stats['pattern_running']:
        time.sleep(0.2)


def breathing(strip, stats, delay=30):
    color = stats['preferred_color']
    while stats['pattern_running']:
        for i in range(270, 630, 2):
            for j in range(strip.numPixels()):
                strip.setPixelColor(j, transform_color(color, (math.sin(math.radians(i)) + 1) / 2))
            strip.show()
            time.sleep(float(delay) / 1000)


def tricolor(strip, stats, delay=1000):
    c1 = Color(0, 255, 0)
    c2 = Color(255, 255, 255)
    c3 = Color(255, 0, 0)
    r1 = 1
    r2 = 2
    r3 = 3
    unit = strip.numPixels() / (r1 + r2 + r3)
    l1 = int(r1 * unit)
    l2 = int(r2 * unit)
    l3 = strip.numPixels() - (l1 + l2)
    while stats['pattern_running']:
        for i in range(l1):
            strip.setPixelColor(i, c1)
        for i in range(l2):
            strip.setPixelColor(l1 + i, c2)
        for i in range(l3):
            strip.setPixelColor(l1 + l2 + i, c3)
        strip.show()
        time.sleep(float(delay) / 1000)


def swipe(strip, stats, delay=20):
    idx = 0
    step = 1
    color = random_color()
    while stats['pattern_running']:
        strip.setPixelColor(idx, color)
        idx += step
        if idx >= strip.numPixels() or idx <= 0:
            color = random_color()
            step = - step
        strip.show()
        time.sleep(float(delay) / 1000)


def random_swipe(strip, stats, delay=30):
    color = random_color()
    indices = []
    while stats['pattern_running']:
        for i in range(strip.numPixels()):
            indices.extend([i])
        while len(indices) > 0:
            strip.setPixelColor(indices.pop(random.randint(0, len(indices) - 1)), color)
            strip.show()
            time.sleep(float(delay) / 1000)
        color = random_color()


def rainbow(strip, stats, wait_ms=20):
    """Draw rainbow that fades across all pixels at once."""
    while stats['pattern_running']:
        for j in range(256):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i+j) & 255))
            strip.show()
            time.sleep(wait_ms/1000.0)


def rainbow_cycle(strip, stats, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    while stats['pattern_running']:
        for j in range(256*iterations):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(wait_ms/1000.0)


def theaterChase(strip, stats, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    color = stats['preferred_color']
    while stats['pattern_running']:
        for j in range(iterations):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i+q, color)
                strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i+q, 0)


def random_color():
    return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def transform_color(color, rate):
    def transform_int(value):
        return min(int(value * rate), 255)
    red, green, blue = get_rgb(color)
    return Color(transform_int(red), transform_int(green), transform_int(blue))


def get_rgb(int_value):
    blue = int_value & 255
    green = (int_value >> 8) & 255
    red = (int_value >> 16) & 255
    return red, green, blue


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)