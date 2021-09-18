import requests

current_league = "Expedition"
item_type_routes = ["UniqueWeapon", "DivinationCard", "UniqueArmour", "UniqueAccessory", "UniqueJewel", "UniqueFlask", "UniqueMap",
                    "Oil", "Incubator", "Scarab", "SkillGem", "Fossil", "Resonator", "Prophecy", "Beast", "Essence"]

currency_type_routes = ["Currency", "Fragment"]

# todo: add stripped function to replace "'" and lower

def price_check(requested_item):  # modes are chaos, exalt, both
    for item_type in item_type_routes:
        request_string = 'https://poe.ninja/api/data/itemoverview?league={league}&type={type}'.format(
            league=current_league, type=item_type)
        r = requests.get(request_string)
        if item_type in ['UniqueWeapon', 'UniqueArmour']:  # items that have different price per links
            if requested_item[-2:] in ['0L', '0l', '5L', '5l', '6l', '6L']:  # checking for specific linkage (0,5,6)
                links = requested_item[-2:]  # last two chars are the num links
                requested_item_name = requested_item[:-3]  # strip the num links and whitespace
                for item in r.json()['lines']:
                    if (item['name'].replace("'", '').lower() in [requested_item_name, requested_item_name.replace("'",
                                                                                                                   '').lower()]) and str(
                            item['links']) == str(requested_item[-2]):
                        return_statement = 'A {arg1} linked {arg2} is currently worth {arg3} chaos orbs.'.format(
                            arg1=str(item['links']), arg2=item['name'], arg3=str(item['chaosValue']))
                        return return_statement
            else:  # if no listed links, assume 0 links
                for item in r.json()['lines']:
                    item['links'] = 0  # bad workaround after api updated to remove links
                    if (item['name'].replace("'", '').lower() in [requested_item,
                                                                  requested_item.replace("'", '').lower()]) and str(
                            item['links']) == str(0):
                        return_statement = 'A {arg1} linked {arg2} is currently worth {arg3} chaos orbs.'.format(
                            arg1=str(item['links']), arg2=item['name'], arg3=str(item['chaosValue']))
                        return return_statement
        else:  # otherwise, links don't matter
            for item in r.json()['lines']:
                if item['name'].replace("'", '').lower() in [requested_item, requested_item.replace("'", '').lower()]:
                    return_statement = '{name} is currently worth {chaos} chaos orbs.'.format(name=item['name'],
                                                                                              chaos=str(
                                                                                                  item['chaosValue']))
                    return return_statement

    for currency_type in currency_type_routes:
        request_string = 'https://poe.ninja/api/data/currencyoverview?league={league}&type={type}'.format(
            league=current_league, type=currency_type)
        r = requests.get(request_string)
        for item in r.json()['lines']:
            if item['currencyTypeName'].replace("'", '').lower() in [requested_item,
                                                                     requested_item.replace("'", '').lower()]:
                return_statement = '{currency} is currently worth {chaos} chaos orbs.'.format(
                    currency=item['currencyTypeName'], chaos=str(item['chaosEquivalent']))
                return return_statement


def price_check_multiple(requested_items, mode):
    pass