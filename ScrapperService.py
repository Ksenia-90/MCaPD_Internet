import json
from datetime import datetime
from HhScrapper import HhScrapper
from SJScrapper import SJScrapper


class ScrapperService:
    def __init__(self, vacancy_on_page, pages_size):
        self._dist_sites = {
            "hh.ru": HhScrapper(vacancy_on_page, pages_size),
            "superjob.ru": SJScrapper(vacancy_on_page, pages_size)
        }

    def scrap_vacancies(self, string_search, list_sites):
        dict_res = {'data': []}
        for site in list_sites:
            if site in self._dist_sites:
                try:
                    result = self._dist_sites.get(site).run(string_search)
                    dict_res.get('data').append({'site_name': site, 'vacancies': result})
                except Exception:
                    print(f'Error scrap site:{site}, by cause:{Exception}')
        dict_res['time_scrapping'] = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        return dict_res


if __name__ == '__main__':
    ss = ScrapperService(1, 1)
    print(ss.scrap_vacancies("программист", ["hh.ru", "superjob.ru"]))
