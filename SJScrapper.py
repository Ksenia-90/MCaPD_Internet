import json
from pprint import pprint

import requests


class SJScrapper:
    def __init__(self, vacancy_on_page, pages_size):
        self._vacancy_on_page = vacancy_on_page
        self._pages_size = pages_size

    def run(self, string_search):
        return sum(list(map(lambda page_num: self.scrap_vacancy_on_page(self.get_page_body(page_num, string_search)),
                            range(1, self._pages_size + 1))), [])

    def get_page_body(self, page_num, string_search):
        url = 'https://www.superjob.ru/jsapi3/0.1/vacancy/'
        params = {
            'filters[keywords]': string_search,
            'page[limit]': self._vacancy_on_page,
            'page[offset]': page_num,
            'include': 'mainInfo.salary,companyInfo,metroStations.lines,town.geo'
        }

        headers = {
            'user-agent': 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/87.0.4280.88 Safari/537.36',
            'accept': '*/*'
        }
        response = requests.get(
            url,
            params=params,
            headers=headers
        )
        if response.status_code == 200:
            return response.text
        else:
            return None

    def scrap_vacancy_on_page(self, text):
        parsed = json.loads(text)
        dict_include = self.build_dictionary_included(parsed['included'])
        return list(map(lambda data: self.build_vacancy(dict_include, data), parsed['data']))

    @staticmethod
    def build_vacancy(dict_included, vacancy_json):
        vacancy = {}
        try:
            vacancy['id'] = vacancy_json['id']
            vacancy_main_info_id = vacancy_json['relationships']['mainInfo']['data']['id']
            vacancy_main_info_attr = dict_included['vacancyMainInfo'][vacancy_main_info_id]['attributes']
            vacancy['vacancy_name'] = vacancy_main_info_attr['profession']
            vacancy['salary'] = {
                'min': vacancy_main_info_attr['minSalary'] if vacancy_main_info_attr['minSalary'] > 0 else None,
                'max': vacancy_main_info_attr['maxSalary'] if vacancy_main_info_attr['maxSalary'] > 0 else None,
                'currency': 'руб'
            }
            if vacancy['salary']['min'] is None and vacancy['salary']['max'] is None:
                vacancy['salary'] = {}
        except KeyError:
            vacancy['vacancy_name'] = None
            vacancy['salary'] = {}

        try:
            vacancy_town_id = vacancy_json['relationships']['town']['data']['id']
            vacancy_town_attr = dict_included['town'][vacancy_town_id]['attributes']
            vacancy['city'] = vacancy_town_attr['name']
        except KeyError:
            vacancy['city'] = {}

        try:
            metro_stations_id = vacancy_json['relationships']['metroStations']['data'][0]['id']
            metro_stations_id_attr = dict_included['metroStation'][metro_stations_id]['attributes']
            vacancy['metro'] = metro_stations_id_attr['label']
        except (KeyError, IndexError):
            vacancy['metro'] = None

        try:
            vacancy_company_info_id = vacancy_json['relationships']['companyInfo']['data']['id']
            vacancy_company_info_attr = dict_included['vacancyCompanyInfo'][vacancy_company_info_id]['attributes']
            vacancy['company'] = vacancy_company_info_attr['name']
        except (KeyError, IndexError):
            vacancy['company'] = None
        return vacancy

    @staticmethod
    def build_dictionary_included(included_json):
        dictionary = {}
        for include in included_json:
            type_dict = dictionary.setdefault(include.get('type'), {})
            type_dict[include['id']] = include
        return dictionary


if __name__ == '__main__':
    sj_scrapper = SJScrapper(1, 1)
    res = sj_scrapper.run('экономист')
    pprint(f'Кол-во вакансий: {len(res)}')
    pprint(res)
