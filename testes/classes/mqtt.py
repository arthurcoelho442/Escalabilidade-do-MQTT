import subprocess
import threading
import logging
import random
import os
from time import sleep
from dotenv import load_dotenv
from paho.mqtt.client import Client
import json

logging.basicConfig(level="INFO")

class MQTT():
    # Descritor
    def __init__(self, path) -> None:        
        load_dotenv(dotenv_path=path+"/.env")

        # config conection
        self.__host             = os.getenv('host', 'localhost')
        self.__attribute        = os.getenv('attr', "value")
        self.__topic            = os.getenv('topic', 'teste')
        self.__port             = int(os.getenv('port', 1883))
        
        # config exec
        self.__numSubs          = int(os.getenv('numSubscriber', 1))
        self.__numPubs          = int(os.getenv('numPublishers', 1))
        self.__simTime          = int(os.getenv('simTime', 10))
        self.__msgTime          = int(os.getenv('msgTime', 100))
        
        # config path result
        self.__path             = os.getenv('result_path', "./")
        self.__stdout_arquivo   = eval(os.getenv('stdout_arquivo', 'False'))
        
        if self.__stdout_arquivo:
            os.makedirs(self.__path, exist_ok=True)
            
        self.__func           = self.__random_num
        
    # SET
    def set_func(self, func):
        self.__func       = func
    
    # Private function
    def __random_num(self, attribute='teste', i=25):
        dic = {attribute: random.randint(i-5, i+5)}
        i   = dic[attribute]
        return dic, i
    
    def __prepare_log_file(self, id, role):
        os.makedirs(self.__path+role, exist_ok=True)
        log_file_path = f"{self.__path+role}{role[:4]}_{id}.log"
        
        with open(log_file_path, 'w') as arquivo:
            arquivo.write("Iniciado\n")
        return open(log_file_path, 'a')
    
    # Public function   
    def sub(self, id, stop_event):
        def on_message(client, userdata, message):
            try:
                mensagem = message.payload.decode('utf-8')
                if(self.__stdout_arquivo and '{' in mensagem and '}' in mensagem):
                    with open(f"{self.__path}/subscribers/sub_{id}.log", 'a') as arquivo:
                        arquivo.write(f"{mensagem}\n")
            except: pass
            
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                if(self.__stdout_arquivo):
                    arquivo = self.__prepare_log_file(id, "/subscribers")
                    arquivo.close()
                client.subscribe(self.__topic)
            else:
                print(f"Falha na conexão, código de erro {rc}")
        
        cmd = f"mosquitto_sub -h {self.__host} -p {self.__port} -t {self.__topic}"
        logging.info(f"Subscriber {id:02d} - {cmd}")
        
        client = Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(self.__host, self.__port)
        
        # Inicia o loop para processar mensagens
        client.loop_start()

        # Espera sinalização do evento de parada
        stop_event.wait()

        # Desconexão do broker MQTT
        client.loop_stop()
        client.disconnect()

    def pub(self, id, stop_event):
        def loop(arquivo = None):
            _, i = self.__func(self.__attribute)
            try:
                while not stop_event.is_set():
                    dic, i = self.__func(self.__attribute, i)
                    
                    os.system(f"{cmd} -m \'{dic}\'")
                    client.publish(self.__topic, dic[self.__attribute])
                    
                    if(arquivo):
                        arquivo.write(f"{dic}\n")
                        
                    sleep(self.__msgTime/1000)
            except Exception as e:
                print(e)
                              
        cmd = f"mosquitto_pub -h {self.__host} -p {self.__port} -t {self.__topic}"
        logging.info(f"Publisher {id:02d} - {cmd}")
        
        client = Client()
        client.connect(self.__host, self.__port)
        if(self.__stdout_arquivo):
            arquivo = self.__prepare_log_file (id, "/publishers")
            loop(arquivo)
            arquivo.write("Terminado")
            arquivo.close()
        else:
            loop()
        client.disconnect()
    
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