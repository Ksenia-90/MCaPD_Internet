import json
from datetime import datetime
from HhScrapper import HhScrapper
from SJScrapper import SJScrapper


class ScrapperService:
    def __init__(self, vacancy_on_page, pages_size):
        self._vacancy_on_page = vacancy_on_page
        self._pages_size = pages_size
        self._hh_scrapper = HhScrapper(vacancy_on_page, pages_size)
        self._sj_scrapper = SJScrapper(vacancy_on_page, pages_size)

    @staticmethod
    def save_json_to_file(file_name, vacancies):
        with open(f'{file_name}', 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, sort_keys=True)

    def run(self, string_search):
        date_time = datetime.now()
        hh_res = self._hh_scrapper.run(string_search)
        sj_res = self._sj_scrapper.run(string_search)
        later = datetime.now()
        dict_res = {
            'time_scrapping': later.strftime('%m/%d/%Y, %H:%M:%S'),
            'data': [
                {'site_name': 'hh.ru', 'vacancies': hh_res},
                {'site_name': 'superjob.ru', 'vacancies': sj_res}
            ]
        }
        date_time.strftime('%m/%d/%Y, %H:%M:%S')
        result_file_name = string_search + '_' + date_time.strftime('%m-%d-%Y_%H_%M_%S') + '.json'
        self.save_json_to_file(result_file_name, dict_res)
        later = datetime.now()
        difference = (later - date_time).total_seconds()
        total_vacancies = len(hh_res) + len(sj_res)
        return f'Время работы скраперра:{difference} секунд, ' \
               f'количество найденых вакансий: {total_vacancies}, файл результата: {result_file_name}'


if __name__ == '__main__':
    string_search_input = input('Введите строку поиска:')
    vacancy_on_page_input = int(input('Введите количество вакансий на странице:'))
    pages_size_input = int(input('Введите количество страниц:'))

    ss = ScrapperService(vacancy_on_page_input, pages_size_input)
    print(ss.run(string_search_input))
