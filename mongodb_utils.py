from pymongo import MongoClient
import json
import mongo_types

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


#~player handles
async def get_all_players()->mongo_types.List[mongo_types.Player]:
    return await player_collection.find({})

#explicação dos tipos no arquivos de tipos
async def get_player(player_id: str) -> mongo_types.Player:
    player_data = player_collection.find_one({"_id": player_id})
    if player_data:
        return player_data
    else:
        raise ValueError(f"Player with ID {player_id} not found")

# ta no nome oq essa função faz
async def get_player_points(id:str)->int:
    #retornara sempre um int por conta da database
    return await player_collection.find({"_id":id}).points

async def get_player_clan(id:str)->mongo_types.Clan:
    clanName = player_collection.find({"_id":id}).clan
    clanData = get_clan(clanName)
    if clanData:
        return clanData
    else:
        raise ValueError(f"Clan {clanName} not found")
    


#~clan handles
async def get_clan(clanName:str)->mongo_types.Clan:
    clan_data = clan_collection.find_one({"name": clanName})
    print(clan_data)
    if clan_data:
        return clan_data
    else:
        raise ValueError(f"Clan {clanName} not found")
    
async def get_all_clans()->mongo_types.List[mongo_types.Clan]:
    return await clan_collection.find({})
