import logging
import subprocess
import os
import threading
from time import sleep

logging.basicConfig(level="INFO")

class MQTT():
    def __init__(self, host, port, topic, attribute) -> None:
        self.host       = host
        self.port       = port
        self.topic      = topic
        self.attribute  = attribute
    
    def config_run(self, func, numSubs, numPubs, msgTime, simTime):
        self.func       = func
        self.numSubs    = numSubs
        self.numPubs    = numPubs
        self.msgTime    = msgTime
        self.simTime    = simTime
    
    def config_path(self, result_path, stdout_arquivo=False):
        if(stdout_arquivo):
            os.makedirs(result_path, exist_ok=True)
            
        self.path    = result_path
        self.stdout_arquivo = stdout_arquivo
    
    def _prepare_log_file(self, id, path, role):
        path += role
        os.makedirs(path+role, exist_ok=True)
        log_file_path = f"{path+role}{role[:4]}_{id}.log"
        
        with open(log_file_path, 'w') as arquivo:
            arquivo.write("Iniciado\n")
        return open(log_file_path, 'a')
            
    def sub(self, id, stop_event):
        cmd = f"mosquitto_sub -h {self.host} -p {self.port} -t {self.topic}"
        logging.info(f"Subscriber {id:02d} - {cmd}")
        
        if(self.stdout_arquivo):
            arquivo = self._prepare_log_file (id, self.path, "/subscribers")
            sub_process = subprocess.Popen(cmd.split(), stdout=arquivo,)
        else:
            sub_process = subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL,)
        
        # Espera sinalização do evento
        stop_event.wait()
        
        # Terminate the subprocess when the stop event is set
        sub_process.terminate()
        sub_process.wait()
        
        if(self.stdout_arquivo):
            arquivo.writelines(["Terminado"])
            arquivo.close() 

    def pub(self, id, stop_event):
        if(self.stdout_arquivo):
            arquivo = self._prepare_log_file (id, self.path, "/publishers")
            log = []
        
        cmd = f"mosquitto_pub -h {self.host} -p {self.port} -t {self.topic}"
        logging.info(f"Publisher {id:02d} - {cmd}")
        
        _, i = self.func(self.attribute)
        try:
            while not stop_event.is_set():
                dic, i = self.func(self.attribute, i)
                
                os.system(f"{cmd} -m \'{dic}\'")
                
                if(self.stdout_arquivo):
                    log.append(f"{dic}\n")
                    
                sleep(self.msgTime/1000)
        except Exception as e:
            print(e, len(i))
        
        if(self.stdout_arquivo):
            log.append("Terminado")
            arquivo.writelines(log)
            arquivo.close()
          
    def run(self):
        multThread, stop_events  = [], []
        
        for qtd, func in [(self.numSubs, self.sub), (self.numPubs, self.pub)]:
            for i in range(qtd):
                stop_event = threading.Event()
                stop_events.append(stop_event)
                thread = threading.Thread(target=func, args=(i+1, stop_event, ))
                multThread.append(thread)
                thread.start()

        # Espera o tempo de execução finalizar
        sleep(self.simTime)

        # Sinaliza todas as threads para pararem
        for event in stop_events:
            event.set()

        # Verifica se todas as threads acabaram 
        for thread in multThread:
            thread.join()