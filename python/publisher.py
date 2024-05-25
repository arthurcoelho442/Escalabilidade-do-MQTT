#!/usr/bin/python

"""
Baseado em 
https://hackmd.io/@ramonfontes/iot-dojot

Modificado para receber como parametro o tempo entre mensagens.
Modificado para aceitar parametros do .env.
"""

import os
import random
import logging

from time import sleep
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv(dotenv_path='../.env')

logging.basicConfig(level="INFO")

i = 25
# Atribui as variáveis
node = os.getenv('host', 'localhost')
topic = os.getenv('topic', 'teste')
attribute = os.getenv('attr', 'temp')
intermsg = os.getenv('msgTime', '1000')

sleep(1)
while True:
    data = random.randint(i-5, i+5)
    i = data

    # Construindo a string JSON manualmente
    msg = '{{"{}": {}}}'.format(attribute, data)

    cmd = "mosquitto_pub -h {} -t {} -m \"{}\"".format(node, topic, msg)
    logging.info(cmd)
    os.system(cmd)
    sleep(int(intermsg)/1000)