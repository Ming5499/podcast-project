import requests
import xmltodict
from pymongo import MongoClient
from utils.constants import *

def process_podcast_data():
    host = MONGODB_HOST   # Default MongoDB host(localhost)
    port = MONGODB_PORT  # Default MongoDB port number(27017)

    # Create a MongoClient instance to connect to MongoDB
    client = MongoClient(host, port)
    # Access a Database
    db = client["podcast"]
    # Access a Collection
    collection = db["podcast"]

    PODCAST_URL = "https://www.marketplace.org/feed/podcast/marketplace/"
    data = requests.get(PODCAST_URL)
    feed = xmltodict.parse(data.text)

    podcast = []
    for i in range(50):
        podcast.append(feed['rss']['channel']['item'][i])

    # Check for duplicate data
    for data in podcast:
        is_duplicate = False
        for doc in collection.find():
            if doc['title'] == data['title']:
                is_duplicate = True
                break
        if not is_duplicate:
            collection.insert_one(data)
