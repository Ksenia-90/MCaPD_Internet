import unicodedata
import requests
from bs4 import BeautifulSoup


class HhScrapper:
    def __init__(self, vacancy_on_page, pages_size):
        self._vacancy_on_page = vacancy_on_page
        self._pages_size = pages_size

    def run(self, string_search):
        return sum(list(map(lambda page_num: self.scrap_vacancy_on_page(self.get_page_body(page_num, string_search)),
                            range(0, self._pages_size))), [])

    def get_page_body(self, page_num, string_search):
        url = 'https://novosibirsk.hh.ru/search/vacancy'
        params = {
            'text': string_search,
            'items_on_page': self._vacancy_on_page,
            'page': page_num
        }
        headers = {
            'host': 'novosibirsk.hh.ru',
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
        parsed_html = BeautifulSoup(text, 'html.parser')
        vacancy_items = parsed_html.find('div', {'data-qa': 'vacancy-serp__results'}) \
            .find_all('div', {'class': 'vacancy-serp-item'})
        return list(map(lambda item: self.scrap_one_item(item), vacancy_items))

    def scrap_one_item(self, item):
        vacancy_df = {}

        # vacancy_name
        vacancy = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        vacancy_df['vacancy_name'] = vacancy.get_text()
        vacancy_df['vacancy_url'] = vacancy['href'].split('?')[0]

        # vacancy_id
        tmp = vacancy_df.get('vacancy_url').split("/")
        vacancy_df['id'] = tmp[len(tmp) - 1]

        # city
        city = item.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText().split(', ')[0]
        vacancy_df['city'] = city

        # metro
        metro = item.find('span', {'class': 'vacancy-serp-item__meta-info'}).findChild()
        if not metro:
            metro = None
        else:
            metro = metro.getText()

        vacancy_df['metro'] = metro

        # company_name
        company = item.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
        vacancy_df['company_name'] = unicodedata.normalize('NFKD', company.get_text())

        # salary
        salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        vacancy_df['salary'] = self.salary_scrapper(salary)
        return vacancy_df

    @staticmethod
    def salary_scrapper(salary):
        salary_df = {}
        if salary is None:
            return salary_df
        else:
            salary_normalize = salary.get_text().replace('\u202f', '')
            salary_normalize_arr = salary_normalize.split(' ')
            salary_df['currency'] = \
                unicodedata.normalize('NFKD', salary_normalize_arr[len(salary_normalize_arr) - 1].replace('.', ''))
            if salary_normalize_arr[0] == 'от':
                salary_df['min'] = salary_normalize_arr[1]
                salary_df['max'] = None
            elif salary_normalize_arr[0] == 'до':
                salary_df['min'] = None
                salary_df['max'] = salary_normalize_arr[1]
            else:
                salary_df['min'] = salary_normalize_arr[0]
                salary_df['max'] = salary_normalize_arr[2]
        return salary_df


if __name__ == '__main__':
    hh_scrapper = HhScrapper(1, 1)
    res = hh_scrapper.run('python')
    print(f'Кол-во вакансий: {len(res)}')
    print(res)
