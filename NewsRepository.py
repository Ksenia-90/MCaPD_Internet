from dotenv import dotenv_values
from pymongo import MongoClient, UpdateOne


class NewsRepository:
    def __init__(self):
        config = dotenv_values('.env')
        uri = config.get('mongo_uri')
        self._mongo_client = MongoClient(uri)
        self._news = self._mongo_client.get_default_database()['news']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("close database connect...")
        self._mongo_client.close()

    # insert if exists
    def insert_news(self, dict_news):
        list_replace_one = self._to_documents(dict_news)
        result = self._news.bulk_write(list_replace_one)
        return result

    @staticmethod
    def _to_documents(dict_news):
        list_update_one = []
        for news_from_site in dict_news['data']:
            source = news_from_site['site_name']
            for one_news in news_from_site['news']:
                one_news['source'] = source
                doc_id = one_news.pop('id', None) + "_" + source
                list_update_one.append(UpdateOne({'_id': doc_id},
                                                 {'$set': one_news},
                                                 upsert=True)
                                       )
        return list_update_one


if __name__ == '__main__':
    repository = NewsRepository()
    dict_news = {
        "time_scrapping": "07/09/2021, 01:08:50",
        "data": [
            {
                "site_name": "hahah.com",
                "news": [
                    {
                        "id": "23523626236",
                        "title": "Fake news",
                        "link": "http://hahah.com/sdgdg"
                    },
                    {
                        "id": "564645645",
                        "title": "Angry bird fligting in Lonfon",
                        "link": "http://hahah.com/berd"
                    }
                ]
            },
            {
                "site_name": "yandex/news.com",
                "news": [
                    {
                        "id": "23523626236",
                        "title": "Fake news",
                        "link": "http://hahah.com/sdgdg"
                    },
                    {
                        "id": "564645645",
                        "title": "Angry bird fligting in Lonfon",
                        "link": "http://hahah.com/berd"
                    }
                ]
            }
        ]
    }
    repository.insert_news(dict_news)

