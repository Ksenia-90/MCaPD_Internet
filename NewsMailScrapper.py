import unicodedata
from datetime import datetime
from pprint import pprint

import requests
from lxml.html import fromstring


class NewsMailScrapper:

    def __init__(self):
        self._base_url = 'https://news.mail.ru/'

    def run(self):
        text = self.get_page_body()
        news = self.parse_text(text)
        return news

    def get_page_body(self, url=None):
        if url is None:
            url = self._base_url
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def parse_text(self, text):
        news = []
        parser_html = fromstring(text)
        news_links = parser_html.xpath('''//ul[@class="list list_type_square list_half js-module"]/
        li/a[contains(@href, "news.mail.ru")]/@href''')
        news_titles = parser_html.xpath('''//ul[@class="list list_type_square list_half js-module"]/
        li/a[contains(@href, "news.mail.ru")]/text()''')

        for i in range(len(news_titles)):
            one_news = {}
            one_news['link'] = news_links[i]
            one_news['title'] = self._prepare_title(news_titles[i])
            one_news['date'] = self._prepare_date(news_links[i])
            one_news['id'] = self._prepare_id(one_news.get('link'))

            news.append(one_news)
        return news

    def _prepare_title(self, title):
        return unicodedata.normalize('NFKD', title)

    def _prepare_link(self, link):
        link = link.split('?')[0]
        if link[0] == "/":
            link = self._base_url + link
        return link

    def _prepare_date(self, link):
        text = self.get_page_body(link)
        parser_html = fromstring(text)
        str_date_time_arr = parser_html.xpath('''(//span[@datetime]/@datetime)[1]''')
        if len(str_date_time_arr)==1:
            str_date_time = str_date_time_arr[0]
            datetime_object = datetime.strptime(str_date_time, '%Y-%m-%dT%H:%M:%S%z')
            return datetime_object

        return None

    def _prepare_id(self, link):
        tmp = link.split("/")
        return tmp[len(tmp) - 1]

if __name__ == '__main__':
    ss = NewsMailScrapper()
    text = ss.get_page_body()
    pprint(ss.parse_text(text))