import json
from tornado import gen, httpclient, ioloop
from pymongo import MongoClient, UpdateOne
from utils import load_yml_config
import time


settings = load_yml_config()
http_client = httpclient.AsyncHTTPClient()
list_appid = [578080, 500]

url = settings.DB_URL
client = MongoClient(url)
db = client.steam_db
collection = db.applist
applist = list(collection.find())
print(len(list(applist)))

@gen.coroutine
def post():
    for appid in applist[:1000]:
        appid = appid['appid']
        try:
            destination = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={}"
            destination = destination.format(appid)
            request = httpclient.HTTPRequest(destination, method="GET")

            response = yield http_client.fetch(request)

            print(json.loads(response.body)['response']['player_count'])
        except KeyboardInterrupt:
            print("Stopped")

        except:
            print("fucked")

if __name__ == '__main__':
    ts = time.time()
    ioloop.IOLoop.current().run_sync(post)
    te = time.time()
    print("Took {:3.1f} sec".format(te-ts))