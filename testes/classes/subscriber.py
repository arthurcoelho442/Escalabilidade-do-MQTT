import logging
import subprocess
from time import sleep

logging.basicConfig(level="INFO")

def sub(num, path, node, port, topic, simTime):
    cmd = f"mosquitto_sub -h {node} -p {port} -t {topic}"
    logging.info(f"USER {num:02d} - {cmd}")
    
    arquivo = open(path + f'/sub_{num}.log', 'w')
    arquivo.writelines(["Iniciado\n"])
    arquivo.close()
    arquivo = open(path + f'/sub_{num}.log', 'a')
    
    sub_process = subprocess.Popen(cmd.split(), stdout=arquivo,)
    
    # Tempo de execução
    sleep(simTime)
    
    # Terminate the subprocess when the stop event is set
    sub_process.terminate()
    sub_process.wait()
    
    arquivo.writelines(["Terminado"])
    arquivo.close() 