import matplotlib.pyplot as plt
import pandas as pd

pasta = "../resultados/"

# Ler os dados do arquivo
data = pd.read_csv(pasta+'mem.dat', delim_whitespace=True, header=None, names=['%CPU', '%MEM'])

# Criar o gráfico
fig, ax1 = plt.subplots()

ax1.set_xlabel('Amostra')
ax1.set_ylabel('%CPU', color='tab:red')
ax1.plot(data['%CPU'], color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')

ax2 = ax1.twinx()  # Instancia um segundo eixo que compartilha o mesmo eixo x
ax2.set_ylabel('%MEM', color='tab:blue')
ax2.plot(data['%MEM'], color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')

fig.tight_layout()  # Para ajustar o layout do gráfico
plt.title('Uso de CPU e Memória do Mosquitto')
plt.savefig(pasta+'mem-graph.png')  # Salva o gráfico como imagem
plt.close()  # Fecha o gráfico