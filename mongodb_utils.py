from pymongo import MongoClient
import json

with open("./config.json") as config_file:
    configs = json.load(config_file)
TOKEN = configs["token"]
CHANNEL_ID = configs["channel_id"]
PROMETHEUS_URL = configs["prometheus_url"]
MONGO_URI = configs["mongo_uri"]
MONGO_DATABASE = configs["mongo_database"]
PLAYER_COLLECTION = configs["player_collection"]
CLANS_COLLECTION = configs["clans_collection"]

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
clan_collection = db[CLANS_COLLECTION]
player_collection = db[PLAYER_COLLECTION]

#player handles
async def get_all_players():
    return await player_collection.find({})

async def get_player():
    return await player_collection.find