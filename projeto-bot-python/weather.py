import requests as rq
import os
from dotenv import load_dotenv
from collections import defaultdict, Counter

load_dotenv('.env')

BASE_URL = "http://api.openweathermap.org"
TOKEN = os.getenv("WEATHER_TOKEN")
ICONS = {
    "01d": "☀️",
    "01n": "☀️",
    "02d": "⛅",
    "02n": "⛅",
    "03d": "☁️",
    "03n": "☁️",
    "04d": "☁️",
    "04n": "☁️",
    "09d": "🌧️",
    "09n": "🌧️",
    "10d": "🌦️",
    "10n": "🌦️",
    "11d": "⛈️",
    "11n": "⛈️",
    "13d": "❄️",
    "13n": "❄️",
    "50d": "🌫️",
    "50n": "🌫️"
}

def geolocalize(cidade: str) -> tuple:
    """Procura a latitude, longitude e país de alguma cidade.

    Args:
        cidade (str): Nome da cidade.

    Returns:
        tuple: Latitude, Longitude e País, nessa ordem.
    """

    res = rq.get(f"{BASE_URL}/geo/1.0/direct?q={cidade}&limit=1&appid={TOKEN}")
    res = res.json()[0]
    return (res['lat'], res['lon'], res['country'])

def weather_now(cidade: str) -> str:
    """Pesquisa o clima atual na cidade desejada.

    Args:
        cidade (str): Nome da cidade.

    Returns:
        str: String formatada contendo: temperaturas, umidade do ar, velocidade do vento, etc.
    """

    lat, lon, pais = geolocalize(cidade)

    if pais == "BR":
        res = rq.get(f"{BASE_URL}/data/2.5/weather?lat={lat}&lon={lon}&appid={TOKEN}&units=metric&lang=pt_br")
        res = res.json()

        return f"""
        Clima atual em 📍{res['name'].capitalize()}: 

{ICONS[res['weather'][0]['icon']]} {res['weather'][0]['description'].capitalize()} - {round(res['main']['temp'])}°C
🌡️ Mínima/Máxima: {res['main']['temp_min']:.1f}°C / {res['main']['temp_max']:.1f}°C
🥵 Sensação térmica: {res['main']['feels_like']:.1f}°C
💧 Umidade do ar: {res['main']['humidity']}%
🍃 Vento: {(res['wind']['speed']*3.6):.2f} Km/h
        """
    
    return "☹️ Não consegui encontrar essa cidade."
    

def weather_forecast(cidade: str) -> str:
    """ Pesquisa pela previsão do tempo para a cidade desejada.

    Args:
        cidade (str): Nome da cidade

    Returns:
        str: String formatada contendo a previsão para os próximos 5 dias.
    """

    lat, lon, pais = geolocalize(cidade)

    if pais == "BR":
        res = rq.get(f"{BASE_URL}/data/2.5/forecast?lat={lat}&lon={lon}&appid={TOKEN}&units=metric&lang=pt_br")
        res = res.json()

        dias = defaultdict(list)
        for item in res["list"]:
            dia = item["dt_txt"].split(" ")[0]
            dias[dia].append(item)

        text = f"Previsão para 📍{cidade.capitalize()}: \n\n"

        for dia, previsoes in dias.items():
            temp = [p["main"]["temp"] for p in previsoes]
            desc = [p["weather"][0]["description"] for p in previsoes]
            icon = [p["weather"][0]["icon"] for p in previsoes]

            desc = Counter(desc).most_common(1)[0][0].capitalize()
            icon = Counter(icon).most_common(1)[0][0]

            temp = max(temp)

            text += f"{dia[-2:]}/{dia[5:7]} - {ICONS[icon]} {desc} - {temp:.0f}°C\n"

        return text
    
    return "☹️ Não consegui encontrar essa cidade."