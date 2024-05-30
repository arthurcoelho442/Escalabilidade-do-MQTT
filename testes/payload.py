import os
from dotenv import load_dotenv
from classes.mqtt import MQTT

path = f'./{os.path.basename(__file__)[:-3]}/'
load_dotenv(dotenv_path=path+".env")

host            = os.getenv('host', 'localhost')
attr            = os.getenv('attr', "value")
topic           = os.getenv('topic', 'teste')
port            = int(os.getenv('port', 1883))
numSubs         = int(os.getenv('numSubscriber', 1))
numPubs         = int(os.getenv('numPublishers', 1))
simTime         = int(os.getenv('simTime', 0))
msgTime         = int(os.getenv('msgTime', 1))
result_path     = os.getenv('result_path', "./")
stdout_arquivo  = eval(os.getenv('stdout_arquivo', 'False'))

        
def increasing_payload(attribute='teste', i=''):
    i   += 'x'
    dic = {attribute: i}
    return dic, i
  
if __name__ == '__main__':
    mqtt = MQTT(host, port, topic, attr)
    if(stdout_arquivo):
        mqtt.set_path(result_path)    
    mqtt.set_func(increasing_payload)
    mqtt.set_run(numSubs, numPubs, msgTime, simTime)
    
    mqtt.run()