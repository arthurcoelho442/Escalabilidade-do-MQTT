#!/bin/bash

delay=1  # intervalo entre as iterações
output_file="./payload/resultados/mem.dat"

mkdir -p ./payload/resultados/

# Limpa o conteúdo do arquivo antes de começar
> "$output_file"

# Executa o script payload.py em segundo plano
python3 ./payload/payload.py &

# Obtém o PID do processo em segundo plano
payload_pid=$!

# Loop enquanto o processo payload.py estiver em execução
while kill -0 $payload_pid 2>/dev/null; do
    # Coleta o uso de CPU e memória do processo 'mosquitto' e adiciona ao arquivo mem.dat
    ps -C mosquitto -o %cpu=,%mem= >> "$output_file"
    
    # Aguarda o intervalo especificado antes da próxima iteração
    sleep $delay
done