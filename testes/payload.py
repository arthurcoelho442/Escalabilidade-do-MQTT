import os
import threading

from dotenv import load_dotenv
from classes.subscriber import sub

path = f'./{os.path.basename(__file__)[:-3]}/'
load_dotenv(dotenv_path=path+".env")

numSubs     = int(os.getenv('numSubscriber', 1))
result_path = os.getenv('result_path', "./")

node    = os.getenv('host', 'localhost')
port    = int(os.getenv('port', 1883))
topic   = os.getenv('topic', 'teste')
simTime = int(os.getenv('simTime', 0))

multThread  = []

try:
    os.mkdir(result_path)
except: pass

for i in range(numSubs):
    thread = threading.Thread(target=sub, args=(i+1, result_path, node, port, topic, simTime, ))
    multThread.append(thread)
    thread.start()
    
# Verifica se todas as threads acabaram 
for thread in multThread:
    thread.join()