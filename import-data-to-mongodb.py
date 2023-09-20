import requests
import xmltodict
from pymongo import MongoClient


host = "localhost"  # Default MongoDB host
port = 27017  # Default MongoDB port number

# Create a MongoClient instance to connect to MongoDB
client = MongoClient(host, port)
#Access a Database
db = client["podcast"]
#Access a Collection
collection = db["podcast"]


PODCAST_URL = "https://www.marketplace.org/feed/podcast/marketplace/"
data = requests.get(PODCAST_URL)
feed = xmltodict.parse(data.text)

podcast =[]
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