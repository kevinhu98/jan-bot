import os

import pymongo
import requests
from dotenv import load_dotenv

load_dotenv()

current_league = 'Ritual'
item_type_routes = [
    'UniqueWeapon',
    'DivinationCard',
    'UniqueArmour',
    'UniqueAccessory',
    'UniqueJewel',
    'UniqueFlask',
    'UniqueMap',
    'Oil',
    'Incubator',
    'Scarab',
    'SkillGem',
    'Fossil',
    'Resonator',
    'Prophecy',
    'Beast',
    'Essence',
]

supported_type_routes = [
    'UniqueWeapon',
    'DivinationCard',
    'UniqueArmour',
    'UniqueAccessory',
    'UniqueJewel',
    'UniqueFlask',
    'Prophecy',
]

item_type_to_db = {
    'UniqueWeapon': 'unique_weapons',
    'DivinationCard': 'divination_cards',
    'UniqueArmour': 'unique_armours',
    'UniqueAccessory': 'unique_accessories',
    'UniqueJewel': 'unique_jewels',
    'UniqueFlask': 'unique_flasks',
    'UniqueMap': 'unique_maps',
    'Oil': 'oils',
    'Incubator': 'incubators',
    'Scarab': 'scarabs',
    'SkillGem': 'skill_gems',
    'Fossil': 'fossils',
    'Resonator': 'resonators',
    'Prophecy': 'prophecies',
    'Beast': 'beasts',
    'Essence': 'essences',
}

try:
    client = pymongo.MongoClient('mongodb+srv://kevin:{arg}@cluster0.8xh0x.mongodb.net/poe.users?retryWrites=true&w=majority'.format(arg=os.getenv('MONGO_PWN')))
    poe_client = client.poe
    print('Successful connection')
except:
    print('no connection')

# div card art path different, i.e. https://web.poecdn.com/image/divination-card/ADabOfInk.png
"""
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
"""
if input('Do you want to delete and recollect all item collections? y/n \n') == 'y':
    # delete and recreate collections
    for item_type in supported_type_routes:
        collection = poe_client[item_type_to_db[item_type]]
        # delete collection
        collection.drop()
        # recreate collection
        collection = poe_client[item_type_to_db[item_type]]

    for item_type in supported_type_routes:
        requestbaseurl = 'https://poe.ninja/api/data/itemoverview?'
        request_string = '{base}league={league}&type={type}'.format(
            base=requestbaseurl,
            league=current_league,
            type=item_type,
        )
        r = requests.get(request_string)
        specific_type_collection = poe_client.get_collection(item_type_to_db[item_type])
        for item in r.json()['lines']:
            item_to_add = {}
            item_to_add['id'] = item['id']
            item_to_add['name'] = item['name']
            item_to_add['itemCategory'] = item_type
            item_to_add['itemBase'] = item['itemType']
            item_to_add['baseType'] = item['baseType']
            item_to_add['levelRequired'] = item['levelRequired']
            item_to_add['icon'] = item['icon']
            item_to_add['baseType'] = item['baseType']
            item_to_add['aliases'] = [item['name'].replace("'", '').lower()]
            item_to_add['implicitModifiers'] = [item['implicitModifiers'][i]['text'] for i in enumerate(item['implicitModifiers'])]
            item_to_add['explicitModifiers'] = [item['explicitModifiers'][i]['text'] for i in enumerate(item['explicitModifiers'])]
            poebaseurl = 'https://pathofexile.gamepedia.com/'
            item_to_add['url'] = poebaseurl + item['name'].replace(' ', '_')
            item_to_add['flavourText'] = item['flavourText']
            if item_type == 'DivinationCard':
                cardbaseurl = 'https://web.poecdn.com/image/divination-card/'
                item_to_add['artUrl'] = '{base}{arg}.png'.format(
                    base=cardbaseurl,
                    arg=item['artFilename'],
                )
                item_to_add['stackSize'] = item['stackSize']
            elif item_type == 'Prophecy':
                item_to_add['prophecyText'] = item['prophecyText']
            print(item_to_add)
            specific_type_collection.insert_one(item_to_add)
