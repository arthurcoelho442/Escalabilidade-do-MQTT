import logging
import subprocess
import os
from time import sleep

logging.basicConfig(level="INFO")

class MQTT():
    def __init__(self, host, port, topic, attribute) -> None:
        self.host       = host
        self.port       = port
        self.topic      = topic
        self.attribute  = attribute
    
    def _prepare_log_file(self, id, path, role):
        path += role
        os.makedirs(path+role, exist_ok=True)
        log_file_path = f"{path+role}{role[:4]}_{id}.log"
        
        with open(log_file_path, 'w') as arquivo:
            arquivo.write("Iniciado\n")
        return open(log_file_path, 'a')
            
    def sub(self, id, stop_event, path, stdout_arquivo=False):
        cmd = f"mosquitto_sub -h {self.host} -p {self.port} -t {self.topic}"
        logging.info(f"Subscriber {id:02d} - {cmd}")
        
        if(stdout_arquivo):
            arquivo = self._prepare_log_file (id, path, "/subscribers")
            sub_process = subprocess.Popen(cmd.split(), stdout=arquivo,)
        else:
            sub_process = subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL,)
        
        # Espera sinalização do evento
        stop_event.wait()
        
        # Terminate the subprocess when the stop event is set
        sub_process.terminate()
        sub_process.wait()
        
        if(stdout_arquivo):
            arquivo.writelines(["Terminado"])
            arquivo.close() 

    def pub(self, id, intermsg, func, stop_event, path, stdout_arquivo=False):
        if(stdout_arquivo):
            arquivo = self._prepare_log_file (id, path, "/publishers")
            log = []
        
        cmd = f"mosquitto_pub -h {self.host} -p {self.port} -t {self.topic}"
        logging.info(f"Publisher {id:02d} - {cmd}")
        
        _, i = func(self.attribute)
        try:
            while not stop_event.is_set():
                dic, i = func(self.attribute, i)
                
                os.system(f"{cmd} -m \'{dic}\'")
                
                if(stdout_arquivo):
                    log.append(f"{dic}\n")
                    
                sleep(intermsg/1000)
        except Exception as e:
            print(e, len(i))
        
        if(stdout_arquivo):
            log.append("Terminado")
            arquivo.writelines(log)
            arquivo.close()