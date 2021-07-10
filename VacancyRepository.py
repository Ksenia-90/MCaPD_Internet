import json

from dotenv import dotenv_values
from pymongo import MongoClient, UpdateOne
from datetime import datetime


class VacancyRepository:
    def __init__(self):
        config = dotenv_values('.env')
        uri = config.get('mongo_uri')
        self._mongo_client = MongoClient(uri)
        self._vacancies = self._mongo_client.get_default_database()['vacancies']

    def test_connect(self):
        return self._vacancies.count()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("close database connect...")
        self._mongo_client.close()

    # insert if exists
    def insert_vacancies(self, dict_vacancies):
        list_replace_one = self._to_documents(dict_vacancies)
        result = self._vacancies.bulk_write(list_replace_one, )
        return result

    @staticmethod
    def _to_documents(dict_vacancies):
        list_replace_one = []
        for vacancies_on_site in dict_vacancies['data']:
            site_name = vacancies_on_site['site_name']
            for vacancy in vacancies_on_site['vacancies']:
                now = datetime.now()
                vacancy['site_name'] = site_name
                vacancy['update_at'] = now
                doc_id = vacancy.pop('id', None) + "_" + site_name
                list_replace_one.append(UpdateOne({'_id': doc_id},
                                                  {'$set': vacancy,
                                                   '$setOnInsert': {'create_at': now}},
                                                  upsert=True)
                                        )
        return list_replace_one

    def get_qt_sum(self, salary, not_exist_salary):
        condition = {"$or": [
            {"salary.min": {"$gte": salary}},
            {"salary.max": {"$gte": salary}}
        ]}

        if not_exist_salary:
            condition = {"$or": [
                {"salary.min": {"$gte": salary}},
                {"salary.max": {"$gte": salary}},
                {"$and": [{"salary.min": {"$exists": False}}, {"salary.max": {"$exists": False}}]}
            ]}

        return list(self._vacancies.find(condition))

