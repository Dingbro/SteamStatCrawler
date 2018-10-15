import requests
from pymongo import MongoClient, UpdateOne
from bson.objectid import ObjectId
import hashlib
import time
import logging
import traceback

from utils import load_yml_config

settings = load_yml_config()
URL_APP_LIST = settings.URL_APP_LIST #"https://api.steampowered.com/ISteamApps/GetAppList/v2"
# URL_CONCURRENT_USER = set#"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def generate_app_id(name):
    str_as_bytes = str.encode(str(name))
    hashed = hashlib.sha256(str_as_bytes).hexdigest()[:24]
    return hashed

def getAppList_handler(event, context):
    ts = time.time()

    try:
        logger.info("Connecting to App list DB...")
        url = event['DB_URL']
        client = MongoClient(url)
        db = client.steam_db
        collection = db.applist
        collection.drop()
        logger.info("Connected to App list DB...")

    except Exception as e:
        logger.error(traceback.format_exc())
        return "DB Connection Failed"

    try:
        logger.info("Requested App List API...")
        url = URL_APP_LIST
        resp = requests.get(url=url)
        resp.raise_for_status()
        list_app = resp.json()['applist']['apps']
        te1 = time.time()
        logger.info("Got App List Data Successfully! Took {:2.2f} sec".format(te1-ts))


    except:
        logger.error(traceback.format_exc())
        return "API Request Failed. Errorcode: {}".format(resp.status_code)

    try:
        logger.info("Updating DB with New App List...")
        cnt = 0
        list_request = list()
        for item in list_app:
            _id = ObjectId(generate_app_id(item['name'] + str(item['appid'])))
            item['_id'] = _id
            list_request.append(
                UpdateOne({'_id': _id}, {'$set': item}, upsert=True))
            cnt += 1

        collection.bulk_write(list_request)
        te2 = time.time()
        logger.info("Updated DB with New App List Successfully! Took {:2.2f} sec".format(te2-te1))

    except:
        logger.error(traceback.format_exc())
        return "Update DB Failed"

    logger.info("Crawling App List Successfully. No. Apps: {}. Took {:2.2f}".format(cnt, te2-ts))
    return "success"


if __name__ == '__main__':
    event = {'DB_URL':"mongodb-url"}
    getAppList_handler(event, None)


