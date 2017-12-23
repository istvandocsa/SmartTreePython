import paho.mqtt.client as mqtt


class Messenger(mqtt.Client):
    def __init__(self, queue):
        super(Messenger, self).__init__()
        self.queue = queue

    def run(self):
        self.connect("localhost", 1883, 60)
        self.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.subscribe("power")
        self.subscribe("brightness")
        self.subscribe("color")
        self.subscribe("pattern")

    def on_message(self, client, userdata, msg):
        print "got message from MQTT: topic " + msg.topic + ", payload " + msg.payload
        self.queue.put(msg)
