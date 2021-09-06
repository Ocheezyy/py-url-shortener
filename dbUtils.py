from pymongo import MongoClient, ReturnDocument
from datetime import datetime as dt2
from pytz import timezone
import helper_methods as hm
import os

tz = timezone('EST')


def check_hash(hash):
    urls = get_conn()
    return True if urls.find({"url_id": hash}).count() > 0 else False

def get_conn():
    client = MongoClient(os.environ.get('MONGO_HOSTNAME'))
    db = client.url_shortener
    coll = db.urls
    return coll

def get_url(hash_id):
    if hash_id is not None:
        urls = get_conn()
        starting_rec = urls.find_one({"url_id": hash_id})
        times_visited = starting_rec['times_visited']

        url_rec = urls.find_one_and_update(
            {"url_id": hash_id}, 
            { '$set': { "times_visited" : times_visited + 1, "last_visited": dt2.now(tz)} }, 
            return_document = ReturnDocument.AFTER
        )
        return url_rec['url']
    else:
        return "No URL recieved"


def create_url(url, base_url):
    if url is not None:
        hash_id = hm.generate_id(5)

        urls = get_conn()
        new_obj = {
            "url_id": hash_id,
            "url": url,
            "date_created": dt2.now(tz),
            "times_visited": 0,
            "last_visited": dt2.now(tz)
        }
        try:
            urls.insert_one(new_obj)
            returnStr = "ocheezy.dev/" + "u/" + new_obj['url_id']
        except Exception as e:
            returnStr = f"{e},, {str(e)}"
        return returnStr
    else:
        return "URL not recieved"


def get_url_stats(hash_id):
    if hash_id is not None:
        urls = get_conn()
        url_data = urls.find_one({"url_id": hash_id}) # TODO: setup
        return url_data