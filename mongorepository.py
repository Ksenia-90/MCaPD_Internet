import hashlib

from dotenv import dotenv_values
from pymongo import MongoClient, UpdateOne


class VacancyRepository:
    def __init__(self):
        config = dotenv_values('.env')
        uri = config.get('mongo_uri')
        self._mongo_client = MongoClient(uri)
        self._vacancies = self._mongo_client.get_default_database()['vacancies']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("close database connect...")
        self._mongo_client.close()

    # insert if exists
    def insert_vacancies(self, vacancy):
        doc_id = hashlib.md5(vacancy['url'].encode('utf-8')).hexdigest()
        self._vacancies.replace_one({"_id": doc_id}, vacancy, upsert=True)

