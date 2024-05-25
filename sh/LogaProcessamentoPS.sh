#!/bin/bash

delay=1; #  intervalo entre as iterações
while true; do
#ps -C <ProgramName> -o pid=,%mem=,vsz= >> /tmp/mem.log
    # Coleta o uso de CPU e memória do processo 'mosquitto' e adiciona ao arquivo mem.dat
    ps -C  mosquitto -o %cpu=,%mem= >> ../resultados/mem.dat

     # Gera um gráfico usando o script Python
     # python3 ../python/gera-grafico.py &

     # Aguarda o intervalo especificado antes da próxima iteração
     sleep $delay
done