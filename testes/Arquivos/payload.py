from classes.mqtt import MQTT
import os

b  = 1
kb = b* 1000
mb = kb * 1000
gb = mb * 1000
        
def increasing_payload(attribute='teste', i=''):
    i   += 'x'*mb
    dic = {attribute: i}
    return dic, i
  
if __name__ == '__main__':
    mqtt = MQTT(f'{os.path.dirname(os.path.abspath(__file__))}/payload')
    mqtt.set_func(increasing_payload)
    mqtt.run()