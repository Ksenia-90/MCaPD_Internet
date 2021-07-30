# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import os
from pprint import pprint

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from dotenv import dotenv_values
from pymongo import MongoClient


class InstagramImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if 'profile_pic_url' in item:
            try:
                yield scrapy.Request(item["profile_pic_url"])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        if results:
            item["img_info"] = [x[1] for x in results if x[0]]
        if 'profile_pic_url' in item:
            del item["profile_pic_url"]
        return item


class ItemPipeline:

    def process_item(self, item, spider):
        # add links
        link_doc = None
        if 'subscribed_from' in item:
            link_doc = {'follower': item['subscribed_from'], 'following': item['pk']}
            del item['subscribed_from']
        elif 'subscribed_to' in item:
            link_doc = {'follower': item['pk'], 'following': item['subscribed_to']}
            del item['subscribed_to']

        if link_doc is not None:
            doc_id = hashlib.md5(
                link_doc['follower'].encode('utf-8') + link_doc['following'].encode('utf-8')).hexdigest()
            self.instagram_links.replace_one({"_id": doc_id}, link_doc, upsert=True)

        doc_id = item['pk']
        self.instagram_users.replace_one({"_id": doc_id}, item, upsert=True)
        return item

    def open_spider(self, spider):
        print("init connect to Db....")
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_PATH = os.path.join(ROOT_DIR, '../.env')
        config = dotenv_values(CONFIG_PATH)
        uri = config.get('mongo_uri')
        self.mongo_client = MongoClient(uri)
        self.instagram_users = self.mongo_client.get_default_database()['instagram_users']
        self.instagram_links = self.mongo_client.get_default_database()['instagram_links']

    def close_spider(self, spider):
        self.mongo_client.close()
        print("Db connect close")
