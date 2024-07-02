from classes.mqtt import MQTT
import os

if __name__ == '__main__':
    mqtt = MQTT(f'{os.path.dirname(os.path.abspath(__file__))}/publisher')
    mqtt.run()