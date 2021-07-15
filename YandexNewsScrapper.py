import hashlib
import re
import unicodedata
from datetime import datetime
from pprint import pprint

import requests
from lxml.html import fromstring


class YandexNewsScrapper:

    def __init__(self):
        self._base_url = 'https://yandex.ru/news/'

    def run(self):
        text = self.get_page_body()
        news = self.parse_text(text)
        return news

    def get_page_body(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'
        }
        response = requests.get(self._base_url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def parse_text(self, text):
        news = []
        parser_html = fromstring(text)
        news_links = parser_html.xpath('//div[@class="mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top"]//a[@class="mg-card__link"]/@href')
        news_titles = parser_html.xpath('//div[@class="mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top"]//h2/text()')
        news_time = parser_html.xpath('//div[@class="mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top"]//span[@class="mg-card-source__time"]/text()')


        for i in range(len(news_titles)):
            one_news = {}
            one_news['link'] = news_links[i]
            one_news['title'] = self._prepare_title(news_titles[i])
            one_news['date'] = self._prepare_date(news_time[i])
            one_news['id'] = self._prepare_id(one_news.get('link'))
            news.append(one_news)
        return news

    def _prepare_title(self, title):
        return unicodedata.normalize('NFKD', title)

    def _prepare_date(self, date):
        date_split = date.split(":")
        return datetime.now().replace(hour=int(date_split[0]),minute=int(date_split[1]),second=0)

    def _prepare_id(self, id):
        return hashlib.md5(id.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    ss = YandexNewsScrapper()
    text = ss.get_page_body()
    pprint(ss.parse_text(text))
