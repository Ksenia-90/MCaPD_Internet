import hashlib

from dotenv import dotenv_values
from pymongo import MongoClient, UpdateOne


class PostsRepository:
    def __init__(self):
        config = dotenv_values('.env')
        uri = config.get('mongo_uri')
        self._mongo_client = MongoClient(uri)
        self._news = self._mongo_client.get_default_database()['vk']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("close database connect...")
        self._mongo_client.close()

    # insert if not exists
    def insert_post(self, posts):
        list_replace_one = self._to_documents(posts)
        result = self._news.bulk_write(list_replace_one)
        return result

    @staticmethod
    def _to_documents(posts):
        list_update_one = []
        for post in posts:
            list_update_one.append(UpdateOne({'_id': hashlib.md5(post['link'].encode('utf-8')).hexdigest()},
                                             {'$set': post},
                                             upsert=True)
                                   )
        return list_update_one
