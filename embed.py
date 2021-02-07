import discord


def create_embed(found_item):  # todo: figure out colors for embed based on item

    if found_item["itemCategory"] in ["UniqueWeapon", "UniqueArmour", "UniqueAccessory"]:
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

    italicized_flavour_text = "*" + found_item["flavourText"] + "*"
    e.add_field(name="\u200b", value=italicized_flavour_text)  # \u200b is zero-width whitespace char

    return e
