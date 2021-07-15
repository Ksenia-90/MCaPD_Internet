import hashlib
import re
import unicodedata
from datetime import datetime
from pprint import pprint

import requests
from lxml.html import fromstring


class LentaScrapper:

    def __init__(self):
        self._base_url = 'https://lenta.ru'

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

        news_links = \
            parser_html.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]| //div[@class="first-item"]/h2 | 
                                        //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                        /a/@href''')
        news_titles = \
            parser_html.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 | 
                                        //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                        /a/text()''')

        news_dates = parser_html.xpath('//section[@class="row b-top7-for-main js-top-seven"]//time/@datetime')

        for i in range(len(news_titles)):
            one_news = {}
            one_news['link'] = self._prepare_link(news_links[i])
            one_news['title'] = self._prepare_title(news_titles[i])
            one_news['date'] = self._prepare_date(news_dates[i], news_links[i])
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

    def _prepare_date(self, date, link):
        result_date_lenta = re.search(r'[0-9]{4}/[0-9]{2}/[0-9]{2}', link)
        result_time = re.search(r'[0-9]{2}:[0-9]{2}', date)

        if result_time is not None and result_date_lenta is not None:
            date_time_str = result_date_lenta.group(0) + " " + result_time.group(0)
            datetime_object = datetime.strptime(date_time_str, '%Y/%m/%d %H:%M')
            return datetime_object

        result_date_mos_lenta = re.search(r'[0-9]{2}-[0-9]{2}-[0-9]{4}', link)
        if result_time is not None and result_date_mos_lenta is not None:
            date_time_str = result_date_mos_lenta.group(0) + " " + result_time.group(0)
            datetime_object = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M')
            return datetime_object

        return None

    def _prepare_id(self, id):
        return hashlib.md5(id.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    ss = LentaScrapper()
    text = ss.get_page_body()
    pprint(ss.parse_text(text))
