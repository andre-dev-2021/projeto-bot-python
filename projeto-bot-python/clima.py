import requests as rq
import os
from dotenv import load_dotenv
from collections import defaultdict, Counter

load_dotenv('.env')
BASE_URL = "http://api.openweathermap.org"
TOKEN = os.getenv("WEATHER_TOKEN")

icone = {
    "01d": 127751,
    "01n": 127750,
    "02d": 9729,
    "02n": 9729,
    "03d": 9729,
    "03n": 9729,
    "04d": 9729,
    "04n": 9729,
    "09d": 127782,
    "09n": 127783,
    "10d": 127782,
    "10n": 127783,
    "11d": 9928,
    "11n": 9928,
    "13d": 10052,
    "13n": 10052,
    "50d": 127745,
    "50n": 127745
}

def get_geolocalizacao(cidade):
    res = rq.get(f"{BASE_URL}/geo/1.0/direct?q={cidade}&limit=1&appid={TOKEN}")
    res = res.json()[0]
    return (res['lat'], res['lon'], res['country'])

def get_clima_atual(cidade):
    lat, lon, pais = get_geolocalizacao(cidade)

    if pais == "BR":
        res = rq.get(f"{BASE_URL}/data/2.5/weather?lat={lat}&lon={lon}&appid={TOKEN}&units=metric&lang=pt_br")
        res = res.json()

        return f"""
            Tempo agora em {chr(128205)} {res['name'].capitalize()}: 

            {chr(icone[res['weather'][0]['icon']])}  {res['weather'][0]['description'].capitalize()} {round(res['main']['temp'])}°C
            {chr(127777)}  Temperatura Mínima/Máxima: {res['main']['temp_min']:.1f}°C / {res['main']['temp_max']:.1f}°C
            {chr(127777)}  Sensação: {res['main']['feels_like']:.1f} °C
            {chr(128167)} Umidade do ar: {res['main']['humidity']} %
            {chr(127811)} Vento: {(res['wind']['speed']*3.6):.2f} Km/h
        """
    
    return f"{chr(10071)} Não foi possivel consultar."
    

def get_previsao(cidade):
    lat, lon, pais = get_geolocalizacao(cidade)

    if pais == "BR":
        res = rq.get(f"{BASE_URL}/data/2.5/forecast?lat={lat}&lon={lon}&appid={TOKEN}&units=metric&lang=pt_br")
        res = res.json()

        dias = defaultdict(list)
        for item in res["list"]:
            dia = item["dt_txt"].split(" ")[0]
            dias[dia].append(item)

        text = f"Previsão para {chr(128205)} {cidade.capitalize()}: \n\n"

        for dia, previsoes in dias.items():
            minimas = [p["main"]["temp_min"] for p in previsoes]
            maximas = [p["main"]["temp_max"] for p in previsoes]
            desc = [p["weather"][0]["description"] for p in previsoes]
            icon = [p["weather"][0]["icon"] for p in previsoes]

            desc = Counter(desc).most_common(1)[0][0].capitalize()
            icon = Counter(icon).most_common(1)[0][0]

            temp_min = min(minimas)
            temp_max = max(maximas)

            text += f"{dia[-2:]}/{dia[5:7]}/{dia[:4]} - {chr(icone[icon])} {desc} - {chr(127777)}  {temp_min:.1f}°C / {temp_max:.1f}°C \n"

        return text
    
    return f"{chr(10071)} Não foi possivel consultar."