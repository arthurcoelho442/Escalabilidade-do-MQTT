#!/bin/bash

source ../.env

# Limpa o caractere de retorno de carro (\r) das variáveis
numPublishers=$(echo "$numPublishers" | tr -d '\r')
simTime=$(echo "$simTime" | tr -d '\r')

mkdir -p ../resultados/
mkdir -p ../resultados/usuarios/

# Loop para iniciar os processos de publicação
for i in $(seq 1 $numPublishers); do
    nohup python3 ../python/publisher.py > "../resultados/usuarios/pub_$i.log" &
done

# Aguarda o tempo de simulação
sleep "$simTime"

# Encerra todos os processos de publicação
killall python3