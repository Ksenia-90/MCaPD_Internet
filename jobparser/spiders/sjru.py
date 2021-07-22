import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://nsk.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=2332']

    def parse(self, response: HtmlResponse):
        links = response.css('div.f-test-vacancy-item a[class*=f-test-link][href^="/vakansii"]::attr(href)').extract()

        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

        next_page = response.css('a.f-test-link-Dalshe::attr(href)').extract_first()

        if next_page:
            yield response.follow(next_page, callback=self.vacancy_parse)

    def vacancy_parse(self, response):
        vacancy_name = response.css('h1 ::text').extract_first()
        vacancy_salary = response.css('span._1h3Zg._2Wp8I._2rfUm._2hCDz ::text').extract()
        vacancy_url = response.url
        vacancy_sourse = 'superjob.ru'

        yield JobparserItem(
        name=vacancy_name,
        salary = vacancy_salary,
        url = vacancy_url,
        sourse = vacancy_sourse
    )
