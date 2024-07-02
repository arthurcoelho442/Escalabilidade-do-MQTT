#!/bin/bash

delay=1  # intervalo entre as iterações
output_file="./resultados/teste_publisher/mem.dat"

mkdir -p ./resultados/teste_publisher

# Limpa o conteúdo do arquivo antes de começar
> "$output_file"

# Executa o script publisher.py em segundo plano
python3 ./Arquivos/publisher.py &

# Obtém o PID do processo em segundo plano
publisher_pid=$!

# Loop enquanto o processo publisher.py estiver em execução
while kill -0 $publisher_pid 2>/dev/null; do
    # Coleta o uso de CPU e memória do processo 'mosquitto' e adiciona ao arquivo mem.dat
    ps -C mosquitto -o %cpu=,%mem= >> "$output_file"
    
    # Aguarda o intervalo especificado antes da próxima iteração
    sleep $delay
done

python3 ./Arquivos/classes/gera-grafico.py ./resultados/teste_publisher/

echo "Scripts executados com sucesso"
exit 0