import discord


def create_embed(found_item):  # todo: figure out colors for embed based on item
    item_category = found_item["itemCategory"]

    if item_category in ["UniqueWeapon", "UniqueArmour", "UniqueAccessory"]:
        e = discord.Embed(title=found_item['name'], url=found_item['url'], description=found_item['itemBase'], color=0xff0000)
        e.set_thumbnail(url=found_item["icon"])
        e.add_field(name="Level Required: ", value=found_item['levelRequired'], inline=False)
        implicit_modifiers, explicit_modifiers = "", ""
        for modifier in found_item['implicitModifiers']:
            implicit_modifiers += modifier + "\n"

        for modifier in found_item['explicitModifiers']:
            explicit_modifiers += modifier + "\n"

        e.add_field(name="Implicit Modifiers:", value=implicit_modifiers, inline=False)
        e.add_field(name="Explicit Modifiers:", value=explicit_modifiers, inline=False)

    elif item_category in ["DivinationCard"]:
        reward = found_item['explicitModifiers'][0]
        reward_type_start = reward.find("<")
        reward_type_end = reward.find(">")
        reward_item_start = reward.find("{")
        reward_item_end = reward.find("}")

        e = discord.Embed(title=found_item['name'], url=found_item['url'], color=0x31DCEF)
        e.set_thumbnail(url=found_item["artUrl"])
        e.add_field(name="Stack Size:", value=found_item["stackSize"], inline=False)

        if reward[reward_type_start + 1: reward_type_end] in ["whiteitem", "uniqueitem", "prophecy"]:
            reward_item_name = reward[reward_item_start + 1: reward_item_end]
            reward_item_url = "https://pathofexile.gamepedia.com/" + reward_item_name.replace("'", "").replace(" ", "_")
            reward_item_embed_value = "[{}]({})".format(reward[reward_item_start + 1: reward_item_end], reward_item_url)
            e.add_field(name="\u200b", value=reward_item_embed_value, inline=False)

        else:
            e.add_field(name="\u200b", value=reward[reward_item_start + 1: reward_item_end], inline=False)

    elif item_category in ["Prophecy"]:
        e = discord.Embed(title=found_item['name'], url=found_item['url'], color=0x9F0FD5)
        e.set_thumbnail(url=found_item["icon"])
        e.add_field(name="\u200b", value=found_item["prophecyText"], inline=False)

    elif item_category in ["UniqueJewel"]:
        pass

    #  adding in flavour text at end
    if "{" in found_item["flavourText"]:
        flavour_text_start = found_item["flavourText"].find("{")
        flavour_text_end = found_item["flavourText"].find("}")
        e.add_field(name="\u200b", value="*" + found_item["flavourText"][flavour_text_start + 1:flavour_text_end] + "*")
    else:
        e.add_field(name="\u200b", value="*" + found_item["flavourText"] + "*")

    return e
