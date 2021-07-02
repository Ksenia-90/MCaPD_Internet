# Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду в данный
# момент для города, название которого получается через input. https://openweathermap.org/current

import pytemperature
import requests
from dotenv import dotenv_values

config = dotenv_values('.env')

city_name = input("Введите название города, например Novosibirsk:")
appid = config.get('appid')

url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={appid}'
response = requests.get(url)
data = response.json()

print(f"В городе {data['name']} {round(pytemperature.k2c(data['main']['temp']), 2)} градусов по Цельсию")
