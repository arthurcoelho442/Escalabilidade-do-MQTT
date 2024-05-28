import logging
import subprocess
import random
import os
from time import sleep

logging.basicConfig(level="INFO")

def sub(num, path, node, port, topic, simTime):
    path += "/subscribers"
    try:
        os.mkdir(path)
    except: pass
    path += f"/sub_{num}.log"
    arquivo = open(path, 'w')
    arquivo.writelines(["Iniciado\n"])
    arquivo.close()
    arquivo = open(path, 'a')
    
    cmd = f"mosquitto_sub -h {node} -p {port} -t {topic}"
    logging.info(f"Subscriber {num:02d} - {cmd}")
    
    sub_process = subprocess.Popen(cmd.split(), stdout=arquivo,)
    
    # Tempo de execução
    sleep(simTime)
    
    # Terminate the subprocess when the stop event is set
    sub_process.terminate()
    sub_process.wait()
    
    arquivo.writelines(["Terminado"])
    arquivo.close() 
    
def pub(num, path, node, port, topic, attribute, intermsg, stop_event):
    path += "/publishers"
    try:
        os.mkdir(path)
    except: pass
    path += f"/pub_{num}.log"
        
    arquivo = open(path, 'w')
    arquivo.writelines(["Iniciado\n"])
    arquivo.close()
    arquivo = open(path, 'a')
    
    i = 25
    attr = '{"%s":' % attribute
    character = '}'
    while not stop_event.is_set():
        data = random.randint(i-5, i+5)
        i = data
        cmd = f"mosquitto_pub -h {node} -p {port} -t {topic} -m \'{attr}{data}{character}\'"
        logging.info(f"Publisher {num:02d} - {cmd}")
        
        sub_process = subprocess.Popen(cmd.split(), stdout=arquivo,)
        sub_process.terminate()
        sub_process.wait()
        sleep(intermsg)
        
    arquivo.writelines(["Terminado"])
    arquivo.close() 