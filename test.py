# main.py
from weather_api import obter_dados_climaticos, formatar_dados

# Obter a localização do usuário
localizacao = input("Nome da cidade: ")

# Obter dados climáticos
dados_climaticos = obter_dados_climaticos(localizacao)

# Imprimir os dados formatados
if dados_climaticos:
    print(formatar_dados(dados_climaticos))
else:
    print("Não foi possível obter os dados climáticos.")
