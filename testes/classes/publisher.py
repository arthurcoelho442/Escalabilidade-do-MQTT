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
port = os.getenv('port', '1883')

topic = os.getenv('topic', 'teste')
attribute = os.getenv('attr', 'value')
intermsg = os.getenv('msgTime', '0')

attr = '{"%s":' % attribute
character = '}'
while True:
    data = random.randint(i-5, i+5)
    i = data
    cmd = "mosquitto_pub -h {} -p {} -t {} -m \'{}{}{}\'".format(node, port, topic, attr, data, character)
    logging.info(cmd)
    os.system(cmd)
    sleep(int(intermsg))