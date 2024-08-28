import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("São_Joaquim.csv", encoding="latin1", delimiter=";", header=None, skiprows=[9])

temperatura = df.iloc[:, 7]  # suponho que a coluna H seja a 8ª coluna (índice 7)

media_temperatura = temperatura.mean()
min_temperatura = temperatura.min()
max_temperatura = temperatura.max()

desvio_padrao = temperatura.std()

print(f"Temperatura média: {media_temperatura:.2f}°C")
print(f"Temperatura mínima: {min_temperatura:.2f}°C")
print(f"Temperatura máxima: {max_temperatura:.2f}°C")
print(f"Desvio padrão: {desvio_padrao:.2f}°C")



plt.boxplot(temperatura)
plt.title("Boxplot da temperatura em São Joaquim em 2023")
plt.xlabel("Temperatura (°C)")
plt.ylabel("")
plt.show()


meses = np.arange(1, 13)  # meses do ano
temperaturas_minimas = []
temperaturas_maximas = []

for mes in meses:
    temperatura_mes = temperatura[df.iloc[:, 0] == mes]  # suponho que a coluna 0 seja a coluna de mês
    temperaturas_minimas.append(temperatura_mes.min())
    temperaturas_maximas.append(temperatura_mes.max())

    plt.bar(meses, temperaturas_minimas, label="Temperatura mínima")
plt.bar(meses, temperaturas_maximas, label="Temperatura máxima")
plt.xlabel("Mês")
plt.ylabel("Temperatura (°C)")
plt.title("Temperaturas mínimas e máximas em São Joaquim em 2023")
plt.legend()
plt.show()