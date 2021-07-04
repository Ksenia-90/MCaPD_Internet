# 1.Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя
# (input), сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев

from pprint import pprint
import requests


def get_response(user_name):
    response = requests.get(f'https://api.github.com/users/{user_name}/repos')
    if response.status_code == 200:
        return response
    else:
        return None


def save_json_to_file(file_name, content):
    with open(f'{file_name}.json', "wb") as f:
        f.write(content)


def print_user_repos(json):
    for repo in json:
        pprint(repo['html_url'])


def get_repos_by_attr(json, attr='html_url'):
    return list(map(lambda repo: repo[attr], json))


def main():
    user_name = input("Введите login:")
    response = get_response(user_name)
    save_json_to_file(user_name, response.content)
    # print url repos
    pprint(get_repos_by_attr(response.json()))
    # print name repos
    pprint(get_repos_by_attr(response.json(), 'name'))


if __name__ == "__main__":
    main()
