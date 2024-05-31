from classes.mqtt import MQTT
import os
        
def increasing_payload(attribute='teste', i=''):
    i   += 'x'
    dic = {attribute: i}
    return dic, i
  
if __name__ == '__main__':
    mqtt = MQTT(f'./{os.path.basename(__file__)[:-3]}')
    mqtt.set_func(increasing_payload)
    mqtt.run()