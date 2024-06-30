#!/bin/bash

delay=1; #  intervalo entre as iterações
output_file="./resultados/mem.dat"

mkdir -p ./resultados/
# Limpa o arquivo antes de começar
> "$output_file"


while true; do
    # Coleta o uso de CPU e memória do processo 'mosquitto' e adiciona ao arquivo mem.dat
    ps -C  mosquitto -o %cpu=,%mem= >> "$output_file"
    
    # Aguarda o intervalo especificado antes da próxima iteração
    sleep $delay
done