# Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду в данный
# момент для города, название которого получается через input. https://openweathermap.org/current

import pytemperature
import requests
from dotenv import dotenv_values


def get_json_response(city_name, app_id):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={app_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_temperature_from_json(json):
    return round(pytemperature.k2c(json['main']['temp']), 2)


def main():
    city_name = input("Введите название города, например Novosibirsk:")
    config = dotenv_values('.env')
    temperature = get_temperature_from_json(get_json_response(city_name, config.get('app_id')))
    print(f"В городе {city_name} {temperature} градусов")


if __name__ == "__main__":
    main()

