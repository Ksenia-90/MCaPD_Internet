import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://novosibirsk.hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=pyhton']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa= 'vacancy-serp__vacancy-title']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()

        if next_page:
            url = response.urljoin(next_page)
            yield response.follow(url, callback=self.vacancy_parse)

    def vacancy_parse(self, response):
        vacancy_name = response.xpath("//h1//text()").extract_first()
        vacancy_salary = response.xpath('''//p[@class="vacancy-salary"]//text()''').extract_first()
        vacancy_url = response.url
        vacancy_sourse = 'hh.ru'

        yield JobparserItem(
        name=vacancy_name,
        salary=vacancy_salary,
        url=vacancy_url,
        sourse=vacancy_sourse
    )
