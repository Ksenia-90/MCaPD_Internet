import os

from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram_scraper import settings
from instagram_scraper.spiders.instagram import InstagramSpider


if __name__ == "__main__":
    load_dotenv(".env")
    login = os.getenv("login")
    password = os.getenv("password")
    app_id = os.getenv("app_id")
    users_input = input("Enter usernames separated by comma:")
    users = users_input.split(",")
    users_strip = [x.strip(' ') for x in users]
    #users_to_parse = nik.fedorchenko, stasgluhoff
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    kwargs = {
        "login": login,
        "password": password,
        "users_to_parse": users_strip,
        "app_id": app_id
    }
    process.crawl(InstagramSpider, **kwargs)

    process.start()





