import os
import random

from time import sleep
from dotenv import load_dotenv
from classes.mqtt import MQTT

path = f'./{os.path.basename(__file__)[:-3]}/'
load_dotenv(dotenv_path=path+".env")

numSubs     = int(os.getenv('numSubscriber', 1))
numPubs     = int(os.getenv('numPublishers', 1))
simTime     = int(os.getenv('simTime', 0))

host        = os.getenv('host', 'localhost')
port        = int(os.getenv('port', 1883))
topic       = os.getenv('topic', 'teste')
attr        = os.getenv('attr', "value")

msgTime     = int(os.getenv('msgTime', 1))
result_path = os.getenv('result_path', "./")
stdout_arquivo = eval(os.getenv('stdout_arquivo', 'False'))

        
def increasing_payload(attribute='teste', i=''):
    dic = {attribute: i}
    i   += 'x'
    return dic, i

def random_num(attribute='teste', i=25):
    dic = {attribute: random.randint(i-5, i+5)}
    i   = dic[attribute]
    return dic, i
  
if __name__ == '__main__':
    mqtt = MQTT(host, port, topic, attr)
    
    mqtt.config_run(random_num, numSubs, numPubs, msgTime, simTime)
    mqtt.config_path(result_path, stdout_arquivo)
    mqtt.run()