import os
import platform
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

# Завантаження змінних середовища
load_dotenv()

def get_system_info():
    print(f"Операційна система: {platform.system()} {platform.release()}")
    print(f"Версія ядра/системи: {platform.version()}")
    print(f"Python: {platform.python_version()}")
    print("-" * 30)

def format_timezone(offset_seconds):
    hours = offset_seconds // 3600
    minutes = (abs(offset_seconds) % 3600) // 60
    sign = "+" if hours >= 0 else "-"
    return f"UTC{sign}{abs(hours):02}:{minutes:02}"

def main():
    get_system_info()

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Помилка: API_KEY не встановлено як змінну середовища у файлі .env!")
        return

    city_input = input("Введіть назву міста: ")
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_input,
        "appid": api_key,
        "units": "metric",
        "lang": "ua"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Обробка даних
        city_name_db = data['name']
        tz_offset = data['timezone']
        tz_str = format_timezone(tz_offset)
        
        # Локальний час запиту
        local_time = datetime.now().astimezone()
        
        # Схід та захід сонця
        sunrise = datetime.fromtimestamp(data['sys']['sunrise'], tz=timezone.utc)
        sunset = datetime.fromtimestamp(data['sys']['sunset'], tz=timezone.utc)
        day_length = sunset - sunrise
        day_hours, remainder = divmod(day_length.seconds, 3600)
        day_minutes = remainder // 60
        
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Вивід результатів
        print(f"Погода у місті {city_input} ({city_name_db}):")
        print(f"Часова зона: {tz_str}")
        print(f"Дата і час запиту (локальний час): {local_time.strftime('%Y-%m-%d %H:%M:%S%z')[:-2] + ':' + local_time.strftime('%z')[-2:]}")
        print(f"Тривалість дня: {day_hours:02}:{day_minutes:02} (г:хв)")
        print(f"Опис: {weather_desc}")
        print(f"Температура: {temp}°C (відчувається як {feels_like}°C)")
        print(f"Вологість: {humidity}%")
        print(f"Швидкість вітру: {wind_speed} м/с")

    except requests.exceptions.RequestException as e:
        print(f"Помилка виконання запиту до API: {e}")

if __name__ == "__main__":
    main()