# Emulação de dispositivos MQTT

Um ambiente para fazer teste de carga e compreender o uso do protocolo MQTT. 

## Conteúdo:

<!-- - `gera-grafico.py` Faz uma publicação em um tópico usando json.
- `mqtt.py` Cria N processos de publisher.py durante um tempo pré determinado
- `.env`  Interrompe todos os processos
- `payload.py` Captura o uso de CPU e memória -->

- `gera-grafico.py` Gera um grafico baseado em dados da cpu e memoria do broker
- `mqtt.py` Classe responsavel por manter a comunicação com o broker, instanciar os publishers e os subscribs
- `.env` Arquivo com as configurações de execução, um para cada teste
- `payload.py`-`pub_sub.py`-`publisher.py` Utilizão a classe mqtt para rodar o teste, podem ser executados sem o script.
- `teste_payload.sh` - `teste_payload.sh` - `teste_publisher.sh` Além de executar o teste, após a execução do .py gera o grafico utilizando o  gera-grafico.py.

## Modo de execução

**Atualização do sistema**
```
sudo apt-get update && apt-get upgrade -y
```

**Adicione o repositorio remoto**
```
git clone https://github.com/arthurcoelho442/Escalabilidade-do-MQTT.git
```

Entre com suas credenciais e as configurações serão baixadas.

**Defina o Email do usuario e o name**
```
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

**Instale a ferramenta de ambiente virtual python**
```
sudo apt install python3.10-venv
```

**Crie um ambiente virtual python**
```
python3 -m venv ./venv
```

**Entre no ambiente virtual**
```
source venv/bin/activate
```

**Instale as dependencias**
```
pip install -r requirements.txt 
```

**Instale o Mosquitto**
```
sudo apt-get install mosquitto mosquitto-clients
```

## Uso

**Entre no ambiente virtual**
```
source venv/bin/activate
```

**Para ver os logs do broker é necessário pará-lo e reinicialo**
```
sudo /etc/init.d/mosquitto stop
sudo mosquitto -v
```

**Para executar o broker em segundo plano basta executar**
```
sudo mosquitto -v -d
```

**Navegue até a pasta de testes**
```
cd testes/
```

Execute o **teste** de acordo com a sua escolha
- Teste do Payload (Testa o máximo de caracteres que é possível enviar pelo publisher):
```
./teste_payload.sh
```
- Teste de Publisher (Analise o consumo de cpu e memória do broker de acordo com o aumento do número de publicações):
```
./teste_publisher.sh
```
- Teste de Publisher e Subscriber (Analise o consumo de cpu e memória do broker de acordo com o aumento do número de inscritos):
```
./teste_pub_sub.sh
```

entre a execução de cada teste reinicie o broker

caso encontre este erro:
`-bash: ./teste_publisher.sh: /bin/bash^M: bad interpreter: No such file or directory`

installe o dos2unix e o execute no arquivo:
```
sudo apt-get install dos2unix

dos2unix teste_publisher.sh
```

As configurações de cada execução podem ser encontradas na pasta /testes/Arquivos/{teste-a-ser-executado}/.env

>Ao final, será gerado uma pasta /testes/resultados com uma pasta do teste executando dentro dela, contendo um arquivo mem.dat com o consumo de memória e cpu do broker, uma imagem mem-graph.png com a analise temporal do arquivo mem.dat e caso a opção **stdout_arquivo** esteja habilitada no .config, seram gerados N arquivos de log para cada publisher e subscriber instanciado.

> `Caso necessite finalizar as threads forçadamente execute`
```
sudo killall python3
```
# Autores
| [<img src="https://avatars.githubusercontent.com/u/56831082?v=4" width=115><br><sub>Arthur Coelho Estevão</sub>](https://github.com/arthurcoelho442) |  [<img src="https://avatars.githubusercontent.com/u/69606747?v=4" width=115><br><sub>Bruno Angeloti Pires</sub>](https://github.com/BrunoAngeloti) |
| :---: | :---: |
