import subprocess
import threading
import logging
import random
import os
from time import sleep

logging.basicConfig(level="INFO")

class MQTT():
    # Descritor
    def __init__(self, host, port, topic, attribute) -> None:
        self.__host           = host
        self.__port           = port
        self.__topic          = topic
        self.__attribute      = attribute
        
        self.__stdout_arquivo = False
        self.__func           = self.__random_num
    
    # SET
    def set_path(self, result_path):
        os.makedirs(result_path, exist_ok=True)
        self.__path    = result_path
        self.__stdout_arquivo = True
          
    def set_func(self, func):
        self.__func       = func
    
    def set_run(self, numSubs=1, numPubs=1, msgTime=100, simTime=10):
        self.__numSubs  = numSubs
        self.__numPubs  = numPubs
        self.__msgTime  = msgTime
        self.__simTime  = simTime
    
    # Private function
    def __random_num(self, attribute='teste', i=25):
        dic = {attribute: random.randint(i-5, i+5)}
        i   = dic[attribute]
        return dic, i
    
    def __prepare_log_file(self, id, path, role):
        path += role
        os.makedirs(path+role, exist_ok=True)
        log_file_path = f"{path+role}{role[:4]}_{id}.log"
        
        with open(log_file_path, 'w') as arquivo:
            arquivo.write("Iniciado\n")
        return open(log_file_path, 'a')
    
    # Public function   
    def sub(self, id, stop_event):
        cmd = f"mosquitto_sub -h {self.__host} -p {self.__port} -t {self.__topic}"
        logging.info(f"Subscriber {id:02d} - {cmd}")
        
        if(self.__stdout_arquivo):
            arquivo = self.__prepare_log_file (id, self.__path, "/subscribers")
            sub_process = subprocess.Popen(cmd.split(), stdout=arquivo,)
        else:
            sub_process = subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL,)
        
        # Espera sinalização do evento
        stop_event.wait()
        
        # Terminate the subprocess when the stop event is set
        sub_process.terminate()
        sub_process.wait()
        
        if(self.__stdout_arquivo):
            arquivo.writelines(["Terminado"])
            arquivo.close() 

    def pub(self, id, stop_event):
        if(self.__stdout_arquivo):
            arquivo = self.__prepare_log_file (id, self.__path, "/publishers")
            log = []
        
        cmd = f"mosquitto_pub -h {self.__host} -p {self.__port} -t {self.__topic}"
        logging.info(f"Publisher {id:02d} - {cmd}")
        
        _, i = self.__func(self.__attribute)
        try:
            while not stop_event.is_set():
                dic, i = self.__func(self.__attribute, i)
                
                os.system(f"{cmd} -m \'{dic}\'")
                
                if(self.__stdout_arquivo):
                    log.append(f"{dic}\n")
                    
                sleep(self.__msgTime/1000)
        except Exception as e:
            print(e, len(i))
        
        if(self.__stdout_arquivo):
            log.append("Terminado")
            arquivo.writelines(log)
            arquivo.close()
    
    def run(self):
        multThread, stop_events  = [], []
        
        for qtd, func in [(self.__numSubs, self.sub), (self.__numPubs, self.pub)]:
            for i in range(qtd):
                stop_event = threading.Event()
                stop_events.append(stop_event)
                thread = threading.Thread(target=func, args=(i+1, stop_event, ))
                multThread.append(thread)
                thread.start()

        # Espera o tempo de execução finalizar
        sleep(self.__simTime)

        # Sinaliza todas as threads para pararem
        for event in stop_events:
            event.set()

        # Verifica se todas as threads acabaram 
        for thread in multThread:
            thread.join()