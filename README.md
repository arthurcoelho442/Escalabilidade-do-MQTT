#Emulação de dispositivos MQTT

Um ambiente para fazer teste de carga e compreender o uso do protocolo MQTT. 

##Conteúdo:

- `publisher.py` Faz uma publicação em um tópico usando json.
- `pubs.sh` Cria N processos de publisher.py durante um tempo pré determinado
- `stopPubs.sh`  Interrompe todos os processos
- `LogaProcessamentoPS.sh` Captura o uso de CPU e memória



##Uso

1. Instalar  Mosquitto e o gnuplot
```
sudo apt-get install mosquitto mosquitto-clients
sudo apt-get install gnuplot
```

2. O broker vai ser inicializado por padrão.  Para ver os logs é necessário
pará-lo e reinicializá-lo.

```
sudo /etc/init.d/mosquitto stop
sudo mosquitto –v
```

3. Configure o nome do tópico em pubs.sh. Por exemplo, temperatura.

4. Abra 1 ou mais terminais e subscreva à este tópico.

```
mosquitto_sub -t temperatura
```

5. Em um novo terminal execute o LogaProcessamento.sh

6. Abra outro terminal, Configure os demais parâmetros em pubs.sh e execute-o. 

7. Ao final, será gerado N arquivos de log e um mem-graph.png com o uso de CPU e memória.