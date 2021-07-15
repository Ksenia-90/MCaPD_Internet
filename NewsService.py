from pprint import pprint

from NewsRepository import NewsRepository
from ScrapperService import ScrapperService

class NewsService:

    @staticmethod
    def upload_news(list_sites):
        scrapper_service = ScrapperService()
        res = scrapper_service.scrap_news(list_sites)
        with NewsRepository() as news_repository:
            return news_repository.insert_news(res)


if __name__ == '__main__':
    news_service = NewsService()
    pprint(news_service.upload_news(["lenta.ru","news.mail.ru", "yandex.news"]).bulk_api_result)
