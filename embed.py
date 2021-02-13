import discord


def create_embed(found_item):
    item_category = found_item['itemCategory']

    if item_category in ['UniqueWeapon', 'UniqueAccessory']:
        e = discord.Embed(title=found_item['name'], url=found_item['url'], description=found_item['itemBase'],
                          color=0xE37D30)
        e.set_thumbnail(url=found_item['icon'])
        e.add_field(name='Level Required: ', value=found_item['levelRequired'], inline=False)
        implicit_modifiers, explicit_modifiers = '', ''
        for modifier in found_item['implicitModifiers']:
            implicit_modifiers = '{impmod}{mod}\n'.format(impmod=implicit_modifiers, mod=modifier)

        for modifier in found_item['explicitModifiers']:
            explicit_modifiers = '{expmod}{mod}\n'.format(expmod=explicit_modifiers, mod=modifier)

        e.add_field(name='Implicit Modifiers:', value=implicit_modifiers, inline=False)
        e.add_field(name='Explicit Modifiers:', value=explicit_modifiers, inline=False)

    elif item_category in ['UniqueArmour']:
        e = discord.Embed(title=found_item['name'], url=found_item['url'], description=found_item['itemBase'],
                          color=0xE37D30)
        e.set_thumbnail(url=found_item['icon'])
        e.add_field(name='Level Required: ', value=found_item['levelRequired'], inline=False)

        if found_item['implicitModifiers']:
            implicit_modifiers = ''
            for i in range(len(found_item['implicitModifiers'])):
                implicit_modifiers = '{impmod}{item}\n'.format(impmod=implicit_modifiers, item=found_item['implicitModifiers'][i])
            e.add_field(name='Implicit Modifiers:', value=implicit_modifiers, inline=False)

        explicit_modifiers = ''
        for i in range(len(found_item['explicitModifiers'])):
            explicit_modifiers = '{expmod}{item}\n'.format(expmod=explicit_modifiers, item=found_item['explicitModifiers'][i])

        e.add_field(name='Explicit Modifiers:', value=explicit_modifiers, inline=False)

    elif item_category in ['UniqueFlask']:
        e = discord.Embed(title=found_item['name'], url=found_item['url'], description=found_item['baseType'],
                          color=0xE37D30)
        e.set_thumbnail(url=found_item['icon'])
        e.add_field(name='Level Required: ', value=found_item['levelRequired'], inline=False)
        implicit_modifiers, explicit_modifiers = '', ''
        for modifier in found_item['implicitModifiers']:
            implicit_modifiers = '{impmod}{mod}\n'.format(impmod=implicit_modifiers, mod=modifier)

        for modifier in found_item['explicitModifiers']:
            explicit_modifiers = '{expmod}{mod}\n'.format(expmod=explicit_modifiers, mod=modifier)

        e.add_field(name='Implicit Modifiers:', value=implicit_modifiers, inline=False)
        e.add_field(name='Explicit Modifiers:', value=explicit_modifiers, inline=False)

    elif item_category in ['DivinationCard']:
        reward = found_item['explicitModifiers'][0]
        reward_type_start = reward.find('<')
        reward_type_end = reward.find('>')
        reward_item_start = reward.find('{')
        reward_item_end = reward.find('}')

        e = discord.Embed(title=found_item['name'], url=found_item['url'], color=0x31DCEF)
        e.set_thumbnail(url=found_item['artUrl'])
        e.add_field(name='Stack Size:', value=found_item['stackSize'], inline=False)

        if reward[reward_type_start + 1: reward_type_end] in ['whiteitem', 'uniqueitem', 'prophecy']:
            reward_item_name = reward[reward_item_start + 1: reward_item_end]
            reward_item_url = 'https://pathofexile.gamepedia.com/{name}'.format(name=reward_item_name.replace("'", '').replace(' ', '_'))
            reward_item_embed_value = '[{}]({})'.format(reward[reward_item_start + 1: reward_item_end], reward_item_url)
            e.add_field(name='\u200b', value=reward_item_embed_value, inline=False)

        else:
            e.add_field(name='\u200b', value=reward[reward_item_start + 1: reward_item_end], inline=False)

    elif item_category in ['Prophecy']:
        e = discord.Embed(title=found_item['name'], url=found_item['url'], color=0x9F0FD5)
        e.set_thumbnail(url=found_item['icon'])
        e.add_field(name='\u200b', value=found_item['prophecyText'], inline=False)

    elif item_category in ['UniqueJewel']:
        e = discord.Embed(title=found_item['name'], url=found_item['url'], color=0xE37D30)
        e.set_thumbnail(url=found_item['icon'])
        explicit_modifiers = ''
        for modifier in found_item['explicitModifiers']:
            explicit_modifiers = '{expmod}{mod}\n'.format(
                expmod=explicit_modifiers,
                mod=modifier,
            )

        e.add_field(
            name='Explicit Modifiers:',
            value=explicit_modifiers,
            inline=False,
        )

    #  adding in flavour text at end
    if '{' in found_item['flavourText']:
        flavour_text_start = found_item['flavourText'].find('{')
        flavour_text_end = found_item['flavourText'].find('}')
        e.add_field(
            name='\u200b',
            value='*{arg}*'.format(
                arg=found_item['flavourText'][flavour_text_start + 1:flavour_text_end],
            ),
        )
    else:
        e.add_field(
            name='\u200b',
            value='*{arg}*'.format(arg=found_item['flavourText']),
        )

    return e
