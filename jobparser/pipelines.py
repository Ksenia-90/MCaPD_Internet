# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import unicodedata
from mongorepository import VacancyRepository

class JobparserPipeline:

    def __init__(self):
        self.client = None

    def process_item(self, item, spider):
        if item['sourse'] == 'hh.ru':
            self.process_item_hh(item, spider)
        else:
            self.process_item_sjru(item, spider)

        with VacancyRepository() as vacancy_repository:
            vacancy_repository.insert_vacancies(item)

        return item

    def process_item_hh(self, item, spider):
        self.parse_salary_hh(item, spider)

    @staticmethod
    def parse_salary_hh(item, spider):
        if item['salary'] is not None:
            salary_normalize = item['salary'].replace('\u202f', 'a')
            salary_normalize_arr = salary_normalize.split(' ')
            item['currency'] = \
                unicodedata.normalize('NFKD', salary_normalize_arr[len(salary_normalize_arr) - 1].replace('.', ''))
            if salary_normalize_arr[0] == 'от':
                item['min_salary'] = salary_normalize_arr[1]
                if salary_normalize_arr[2] == 'до':
                    item['max_salary'] = salary_normalize_arr[3]
            else:
                item['min_salary'] = None
                item['max_salary'] = None
            del item['salary']

    @staticmethod
    def process_item_sjru(item, spider):
        item['min_salary'] = None
        item['max_salary'] = None
        salary = item['salary']
        for i in range(len(salary)):
            salary[i] = salary[i].replace(u'\xa0', u'')

        if salary[0] == 'от':
            item['min_salary'] = salary[2]

        if salary[0] == 'до':
            item['max_salary'] = salary[2]

        if len(salary[0]) > 0 and salary[0][0].isdigit():
            item['min_salary'] = salary[0]
            item['max_salary'] = salary[4]

        del item['salary']

        if item['min_salary'] is not None:
            if item['min_salary'][-1] == ".":
                item['currency'] = item['min_salary'][-4:-1]
                item['min_salary'] = item['min_salary'][:-4]

        if item['max_salary'] is not None:
            if item['max_salary'][-1] == ".":
                item['max_salary'] = item['max_salary'][:-4]
                if item['currency'] is None:
                    item['currency'] = item['max_salary'][:-4]

    def extract_currency(self, salary_item):
        if salary_item is not None:
            if salary_item[-1] == ".":
                return salary_item[-4:-1]

        return None

# closing database conection on closing spider
    def close_spider(self):
        self.client.close()