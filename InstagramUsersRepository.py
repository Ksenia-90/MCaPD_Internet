from pprint import pprint

from dotenv import dotenv_values
from pymongo import MongoClient


class InstagramUsersRepository:
    def __init__(self):
        config = dotenv_values('.env')
        uri = config.get('mongo_uri')
        self._mongo_client = MongoClient(uri)
        self._instagram_users = self._mongo_client.get_default_database()['instagram_users']
        self._instagram_links = self._mongo_client.get_default_database()['instagram_links']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("close database connect...")
        self._mongo_client.close()


    def get_following_by_username(self, username):
        # find pk by username
        user = self._instagram_users.find_one({"username": username})
        if user is not None:
            # find pk's followers
            followers = self._instagram_links.find({"follower": user['pk']})
            followers_pk = list(map(lambda user: user['following'], list(followers)))
            return list(self._instagram_users.find({"pk": {"$in": followers_pk}}))



    def get_followers_by_username(self, username):
        # find pk by username
        user = self._instagram_users.find_one({"username": username})
        if user is not None:
            # find pk's followers
            following = self._instagram_links.find({"following": user['pk']})
            following_pk = list(map(lambda user: user['follower'], list(following)))
            return list(self._instagram_users.find({"pk": {"$in": following_pk}}))

