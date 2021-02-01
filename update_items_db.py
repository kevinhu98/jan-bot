import pymongo
import os
import requests
from dotenv import load_dotenv

load_dotenv()

current_league = "Ritual"
item_type_routes = ["UniqueWeapon", "DivinationCard", "UniqueArmour", "UniqueAccessory", "UniqueJewel", "UniqueFlask", "UniqueMap",
                    "Oil", "Incubator", "Scarab", "SkillGem", "Fossil", "Resonator", "Prophecy", "Beast", "Essence"]

try:
    client = pymongo.MongoClient("mongodb+srv://kevin:" + os.getenv('MONGO_PW') + "@cluster0.8xh0x.mongodb.net/poe.users?retryWrites=true&w=majority")
    poe_client = client.poe
    poe_items = poe_client.items
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
    for item in r.json()['lines']:
        print(item["id"])
        print(item['name'])
        print(item[''])
        print(item["levelRequired"])
        print(item["icon"])
        print(item["baseType"])
        for modifier in item["implicitModifiers"][0]:
            print(modifier)
        for modifier in item["explicitModifiers"][0]:
            print(modifier)
        print(item["flavourText"])
        print(item["itemType"])
        break
    print('new item +++++')