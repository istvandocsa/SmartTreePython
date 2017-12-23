# !/usr/bin/python
from Queue import Queue
from classes.led_controller import LedController
from classes.messenger import Messenger

import signal
import sys

q = Queue()
led_controller = LedController(q)
messenger = Messenger(q)


def signal_handler(signal, frame):
    led_controller.wipe()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
led_controller.run()
messenger.run()
