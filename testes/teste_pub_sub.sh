#!/bin/bash

delay=1  # intervalo entre as iterações
output_file="./resultados/teste_pub_sub/mem.dat"

mkdir -p ./resultados/teste_pub_sub

# Limpa o conteúdo do arquivo antes de começar
> "$output_file"

# Executa o script pub_sub.py em segundo plano
python3 ./Arquivos/pub_sub.py &

# Obtém o PID do processo em segundo plano
pub_sub_pid=$!

# Loop enquanto o processo pub_sub.py estiver em execução
while kill -0 $pub_sub_pid 2>/dev/null; do
    # Coleta o uso de CPU e memória do processo 'mosquitto' e adiciona ao arquivo mem.dat
    ps -C mosquitto -o %cpu=,%mem= >> "$output_file"
    
    # Aguarda o intervalo especificado antes da próxima iteração
    sleep $delay
done

python3 ./Arquivos/classes/gera-grafico.py ./resultados/teste_pub_sub/

echo "Scripts executados com sucesso"
exit 0