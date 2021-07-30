# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramScraperItem(scrapy.Item):
    pk = scrapy.Field()
    username = scrapy.Field()
    full_name = scrapy.Field()
    profile_pic_url = scrapy.Field()
    subscribed_to = scrapy.Field()
    subscribed_from = scrapy.Field()
    img_info = scrapy.Field()
