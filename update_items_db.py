import pymongo
import os
import requests
from dotenv import load_dotenv

load_dotenv()

current_league = "Ritual"
item_type_routes = ["UniqueWeapon", "DivinationCard", "UniqueArmour", "UniqueAccessory", "UniqueJewel", "UniqueFlask", "UniqueMap",
                    "Oil", "Incubator", "Scarab", "SkillGem", "Fossil", "Resonator", "Prophecy", "Beast", "Essence"]

item_type_to_db = {"UniqueWeapon": "unique_weapons",
                   "DivinationCard": "divination_cards",
                   "UniqueArmour": "unique_armors",
                   "UniqueAccessory": "unique_accessories",
                   "UniqueJewel": "unique_jewels",
                   "UniqueFlask": "unique_flasks",
                   "UniqueMap": "unique_maps",
                   "Oil": "oils",
                   "Incubator": "incubators",
                   "Scarab": "scarabs",
                   "SkillGem": "skill_gems",
                   "Fossil": "fossils", 
                   "Resonator": "resonators",
                   "Prophecy": "prophecies",
                   "Beast": "beasts",
                   "Essence": "essences"}
try:
    client = pymongo.MongoClient("mongodb+srv://kevin:" + os.getenv('MONGO_PW') + "@cluster0.8xh0x.mongodb.net/poe.users?retryWrites=true&w=majority")
    poe_client = client.poe
    print('Successful connection')
except:
    print('no connection')

# div card art path different, i.e. https://web.poecdn.com/image/divination-card/ADabOfInk.png
'''
item:

poeninjaID
name
item_type_route
baseType
levelRequired
itemType
flavourText
icon
implicitModifiers
explicitModifiers
aliases
'''
for item_type in item_type_routes:
    request_string = 'https://poe.ninja/api/data/itemoverview?league={}&type={}'.format(current_league, item_type)
    r = requests.get(request_string)
    poe_collection = poe_client.get_collection(item_type_to_db[item_type])
    for item in r.json()['lines']:
        item_to_add = {}
        item_to_add['id'] = item['id']
        item_to_add['name'] = item['name']
        item_to_add['itemType'] = item_type
        item_to_add['baseType'] = item['baseType']
        item_to_add['levelRequired'] = item["levelRequired"]
        item_to_add['itemType'] = item['itemType']
        item_to_add['icon'] = item["icon"]
        item_to_add['baseType'] = item["baseType"]
        item_to_add['aliases'] = []
        item_to_add['implicitModifiers'] = [item["implicitModifiers"][i]['text'] for i in range(len(item["implicitModifiers"]))]
        item_to_add['explicitModifiers'] = [item["explicitModifiers"][i]['text'] for i in range(len(item["explicitModifiers"]))]

        print(item_to_add)
        poe_collection.insert_one(item_to_add)
    break