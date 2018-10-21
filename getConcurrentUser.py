import requests
from pymongo import MongoClient, UpdateOne
from bson.objectid import ObjectId
import hashlib
import time
import logging
import traceback
from tornado import gen, httpclient, ioloop

from utils import load_yml_config

settings = load_yml_config()
URL_APP_LIST = settings.URL_APP_LIST
URL_CONCURRENT_USER = settings.URL_CONCURRENT_USER

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

http_client = httpclient.AsyncHTTPClient()


def generate_app_id(name):
    str_as_bytes = str.encode(str(name))
    hashed = hashlib.sha256(str_as_bytes).hexdigest()[:24]
    return hashed

def getConcurrentUser_handler(event, context):
    pass

if __name__ == '__main__':
    event = {'DB_URL':"mongodb-url"}
    getConcurrentUser_handler(event, None)


