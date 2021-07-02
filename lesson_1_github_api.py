# 1.Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя
# (input), сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев

from pprint import pprint

import requests

username = input("Введите login:")

response = requests.get(f'https://api.github.com/users/{username}/repos')

with open(f'{username}.json', "wb") as f:
    f.write(response.content)

for repo in response.json():
    pprint(repo['html_url'])
