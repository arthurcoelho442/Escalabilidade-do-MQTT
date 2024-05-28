import os
import threading
from time import sleep

from dotenv import load_dotenv
from classes.subscriber import sub
from classes.subscriber import pub

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

multThread, stop_events  = [], []

try:
    os.mkdir(result_path)
except: pass

# for i in range(numSubs):
#     thread = threading.Thread(target=sub, args=(i+1, result_path, host, port, topic, simTime, ))
#     multThread.append(thread)
#     thread.start()
    
# # Verifica se todas as threads acabaram 
# for thread in multThread:
#     thread.join()

for i in range(numPubs):
    stop_event = threading.Event()
    stop_events.append(stop_event)
    thread = threading.Thread(target=pub, args=(i+1, result_path, host, port, topic, attr, msgTime, stop_event, ))
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