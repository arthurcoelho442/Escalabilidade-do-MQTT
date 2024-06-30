from classes.mqtt import MQTT
import os
import sys

b  = 1
kb = b* 1000
mb = kb * 1000
gb = mb * 1000
        
def increasing_payload(attribute='teste', i=''):
    i   += 'x'*mb
    dic = {attribute: i}
    return dic, i
  
if __name__ == '__main__':
    mqtt = MQTT(f'./{os.path.basename(__file__)[:-3]}')
    mqtt.set_func(increasing_payload)
    mqtt.run()