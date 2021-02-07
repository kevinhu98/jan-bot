import discord

def createEmbed(found_item):  # todo: figure out colors for embed based on item

    if found_item["itemCategory"] in ["UniqueWeapon", "UniqueArmour", "UniqueJewelery"]:
        e = discord.Embed(title=found_item['name'], url=found_item['url'], description=found_item['itemBase'], color=0xff0000)
        e.set_thumbnail(url=found_item["icon"])
        e.add_field(name="Level Required: ", value=found_item['levelRequired'], inline=False)
        implicitModifiers, explicitModifiers = "", ""
        for modifier in found_item['implicitModifiers']:
            implicitModifiers += modifier + "\n"

        for modifier in found_item['explicitModifiers']:
            explicitModifiers += modifier + "\n"
        '''
        e.add_field(name="\u200b", value="Implicit Modifiers:", inline=False)
        for modifier in found_item['implicitModifiers']:
            e.add_field(name="\u200b", value=modifier, inline=False)
        e.add_field(name="\u200b", value="Explicit Modifiers:", inline=False)
        for modifier in found_item['explicitModifiers']:
            e.add_field(name="\u200b", value=modifier, inline=False)
        '''
        e.add_field(name="Implicit Modifiers:", value=implicitModifiers, inline=False)
        e.add_field(name="Explicit Modifiers:", value=explicitModifiers, inline=False)
    e.add_field(name="sad", value=found_item["flavourText"])

    return e
