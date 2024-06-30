#!/bin/bash

delay=1  # intervalo entre as iterações
output_file="./resultados/payload/mem.dat"

mkdir -p ./resultados/payload

# Limpa o conteúdo do arquivo antes de começar
> "$output_file"

# Executa o script payload.py em segundo plano
python3 ./Arquivos/payload.py &

# Obtém o PID do processo em segundo plano
payload_pid=$!

# Loop enquanto o processo payload.py estiver em execução
while kill -0 $payload_pid 2>/dev/null; do
    # Coleta o uso de CPU e memória do processo 'mosquitto' e adiciona ao arquivo mem.dat
    ps -C mosquitto -o %cpu=,%mem= >> "$output_file"
    
    # Aguarda o intervalo especificado antes da próxima iteração
    sleep $delay
done

python3 ./Arquivos/classes/gera-grafico.py ./resultados/payload/

echo "Scripts executados com sucesso"
exit 0