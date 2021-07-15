import json
from datetime import datetime
from LentaScrapper import LentaScrapper
from NewsMailScrapper import NewsMailScrapper
from YandexNewsScrapper import YandexNewsScrapper


class ScrapperService:
    def __init__(self):
        self._dist_sites = {
            'lenta.ru': LentaScrapper(),
            'yandex.news': YandexNewsScrapper(),
            'news.mail.ru': NewsMailScrapper()
        }

    def scrap_news(self, list_sites):
        dict_res = {'data': []}
        for site in list_sites:
            if site in self._dist_sites:
                try:
                    result = self._dist_sites.get(site).run()
                    dict_res.get('data').append({'site_name': site, 'news': result})
                except Exception:
                    print(f'Error scrap site:{site}, by cause:{Exception}')
            else:
                print(f'missing scrapper: {site}')

        dict_res['time_scrapping'] = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        return dict_res


if __name__ == '__main__':
    ss = ScrapperService()
    print(ss.scrap_news(["lenta.ru", 'yandex.news', 'news.mail.ru']))
