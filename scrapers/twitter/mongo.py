# from tweepy import Stream
from tweepy import OAuthHandler
# from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Cursor
import credentials
import json
import requests
import os
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://Vasu:htccg321@cluster0-miow4.mongodb.net/flipkart-grid?retryWrites=true&w=majority")

database = client["flipkart-grid"]
collection = database["twitter_data"]


def authenticate():
    auth = OAuthHandler(credentials.api_key, credentials.api_key_secret)
    auth.set_access_token(credentials.access_token,
                          credentials.access_token_secret)
    return auth


# import base64
# with open("yourfile.ext", "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read())


def twitter_client(num, twitter_user=None):
    auth = authenticate()
    client_handler = API(auth)
    return list(Cursor(client_handler.user_timeline, id=twitter_user).items(num))


fashion_handles = ['FASHlONABLE', 'SHEIN_official', 'VogueParis', 'Refinery29',
                   'TimesFashion', 'AmazonFashionIn']

num = 200


def download_image(pic_urls, handle, id):
    if not os.path.exists("./data"):
        os.mkdir("./data")
    if not os.path.exists("./data/{0}".format(handle)):
        os.mkdir("./data/{0}".format(handle))
    for i, pic_url in enumerate(pic_urls):
        img_data = requests.get(pic_url).content
        with open('./data/{0}/{1}_{2}.jpg'.format(handle, id, i), 'wb') as handler:
            handler.write(img_data)


extraction = {}
k = 0
for handle in fashion_handles:
    # extraction[handle] = {}

    data = twitter_client(num, handle)
    for i, tweet in enumerate(data):
        obj = {}
        json_str = tweet._json
        # try:
        urls = []
        try:
            urls.extend(twt['media_url'] for twt in json_str['extended_entities']['media'])
        except:
            pass
        if urls:
            #     download_image(urls, handle, json_str['id'])
            obj['id'] = json_str['id']
            obj['favorite_count'] = json_str['favorite_count']
            obj['text'] = json_str['text']
            obj['created_at'] = json_str['created_at']
            obj["media_urls"] = urls
            obj['source'] = handle
            # extraction[handle][k] = obj
            # k += 1
            collection.insert_one(obj)
        # except:
        #     pass
        print(handle, "tweet", i)
    print("Completed - ", handle)

with open("dump.json", 'w+') as file:
    json.dump(extraction, file)
    # file.write(json.dumps(extraction))
