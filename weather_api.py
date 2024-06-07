import requests
from datetime import datetime


def obter_dados_climaticos(localizacao: str):
    app_key = "6ddfa73781ed9e02957b12b224d7b20f"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    parametros = {
        "q": localizacao,
        "appid": app_key,
        "units": "metric",
        "lang": "pt_br"
    }

    resposta = requests.get(base_url, params=parametros)
    if resposta.status_code == 200:
        dados_climaticos = resposta.json()
        return dados_climaticos
    else:
        print(f"Error {resposta.status_code}: {resposta.reason}")
        return None


def formatar_dados(dados):
    cidade = dados.get("name")
    pais = dados.get("sys", {}).get("country")
    temperatura = dados.get("main", {}).get("temp")
    umidade = dados.get("main", {}).get("humidity")
    pressao = dados.get("main", {}).get("pressure")
    velocidade_vento = dados.get("wind", {}).get("speed")
    direcao_vento = dados.get("wind", {}).get("deg")
    descricao = dados.get("weather", [])[0].get("description")
    visibilidade = dados.get("visibility")
    nascer_sol = dados.get("sys", {}).get("sunrise")
    por_sol = dados.get("sys", {}).get("sunset")
    horario_atual = dados.get("dt")

    # Converte timestamps para formato legível
    nascer_sol = datetime.fromtimestamp(nascer_sol).strftime('%Y-%m-%d %H:%M:%S') if nascer_sol else "N/A"
    por_sol = datetime.fromtimestamp(por_sol).strftime('%Y-%m-%d %H:%M:%S') if por_sol else "N/A"
    horario_atual = datetime.fromtimestamp(horario_atual).strftime('%Y-%m-%d %H:%M:%S') if horario_atual else "N/A"

    dados_formatados = (
        f"Informações climáticas para {cidade}, {pais}:\n"
        f"Data e Hora: {horario_atual}\n"
        f"Descrição: {descricao.capitalize()}\n"
        f"Temperatura: {temperatura}°C\n"
        f"Umidade: {umidade}%\n"
        f"Pressão: {pressao} hPa\n"
        f"Velocidade do Vento: {velocidade_vento} m/s\n"
        f"Direção do Vento: {direcao_vento}°\n"
        f"Visibilidade: {visibilidade} m\n"
        f"Nascer do Sol: {nascer_sol}\n"
        f"Pôr do Sol: {por_sol}\n"
    )
    return dados_formatados
