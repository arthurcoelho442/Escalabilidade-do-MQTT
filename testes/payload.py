import os
import threading
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
stdout_arquivo = eval(os.getenv('stdout_arquivo', False))

        
def increasing_payload(attribute='teste', i=''):
    dic = {attribute: i}
    i   += 'x'
    return dic, i

def random_num(attribute='teste', i=25):
    dic = {attribute: random.randint(i-5, i+5)}
    i   = dic[attribute]
    return dic, i
  
if __name__ == '__main__':
    multThread, stop_events  = [], []
    obj = random_num
    mqtt = MQTT(host, port, topic, attr)
    
    if(stdout_arquivo):
        try:
            os.mkdir(result_path)
        except Exception as e: pass

    for i in range(numSubs):
        stop_event = threading.Event()
        stop_events.append(stop_event)
        thread = threading.Thread(target=mqtt.sub, args=(i+1, stop_event, result_path, stdout_arquivo, ))
        multThread.append(thread)
        thread.start()

    for i in range(numPubs):
        stop_event = threading.Event()
        stop_events.append(stop_event)        
        thread = threading.Thread(target=mqtt.pub, args=(i+1, msgTime, obj, stop_event, result_path, stdout_arquivo, ))
        multThread.append(thread)
        thread.start()

    # Espera o tempo de execução finalizar
    sleep(simTime)

    # Sinaliza todas as threads para parar
    for event in stop_events:
        event.set()

    # Verifica se todas as threads acabaram 
    for thread in multThread:
        thread.join()