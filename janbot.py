# bot.py
import os
import discord
import robin_stocks
import requests
import robin_stocks
from discord.ext import commands
from dotenv import load_dotenv
import glob
import sys
import random
import time
import asyncio

from embed import create_poe_item_embed
from price_check import price_check
from ext.utilities import *
from cogs.bet import Bet
from cogs.poe_inventory import Inventory
from cogs.stocks import Stocks
from cogs.music import Music
load_dotenv()


# setting up discord api info
token = os.getenv('DISCORD_TOKEN')

'''
# setting up robinhood api info
login = robin_stocks.login(os.getenv('ROBINHOOD_LOGIN'), os.getenv('ROBINHOOD_PW'))
'''

# setting up richard image paths
richardPicDir = glob.glob('richardpics/*')
richardPics = []
for path in richardPicDir:
    richardPics.append(path.replace('\\', '/'))


# setting up interview questions
with open('text_file_resources/interviewquestions.txt') as f:
    interviewQuestions = [question for question in f]


# setting up poe ninja routes and league info
# todo: auto update current_league
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


currency_type_routes = ['Currency', 'Fragment']


# connect to db

poe_users = connectToPoeDB().users
bot = commands.Bot(command_prefix='', help_command=None)
bot.add_cog(Inventory(bot))
bot.add_cog(Stocks(bot))
bot.add_cog(Music(bot))
bot.add_cog(Bet(bot))

@bot.command(name="help")  # todo: make help embed multi-page
async def help_embed(ctx):
    """
    Displays a discord embed object with a list of commands
    :param ctx:
    :return: Prints an embed object
    """
    embedVar = discord.Embed(title='Janbot Commands', description='look at that boy go', color=0xff0000)
    embedVar.add_field(name="c 'currency'", value='Returns the chaos orb equivalent of currency', inline=False)
    embedVar.add_field(name="e 'currency'", value='Returns the exalted orb equivalent of currency', inline=False)
    embedVar.add_field(name="ce 'currency'", value='Returns the total exalted and chaos orb equivalent of currency', inline=False)
    embedVar.add_field(name="ci 'item' 'optional: 0l,5l,6l'", value='Returns the chaos orb equivalent of item', inline=False)
    embedVar.add_field(name="ei 'item'", value='Returns the exalted orb equivalent of item', inline=False)
    embedVar.add_field(name="id 'item", value='Info about item (supports uniques, divination cards, and prophecies)', inline=False)
    embedVar.add_field(name='!stonks', value='Displays portfolio value', inline=False)
    embedVar.add_field(name='!positions', value='Displays account positions', inline=False)
    embedVar.add_field(name='!richard', value='Random richard picture', inline=False)
    await ctx.send(embed=embedVar)


@bot.command(name='ci')
async def item_chaos_price(ctx, *args):
    """
    Given any item, displays the chaos value of object
    :param ctx:
    :param args: first argument is the name of the item, second optional argument is number of links if possible
    :return: Returns string with chaos value
    """
    requested_item = ' '.join(args)
    if price_check(requested_item):
        return await ctx.send(price_check(requested_item))

    else:
        return_statement = 'Cannot find: {item}. \nPlease make sure that you are typing the full name of the item.'.format(item=requested_item)
        await ctx.send(return_statement)


@bot.command(name='ei')
async def item_exalt_price(ctx, *args):
    """
    Given any item, displays the exalt value of object
    :param ctx:
    :param args: first argument is the name of the item, second optional argument is number of links if possible
    :return: Returns string with exalt value
    """
    requested_item = ' '.join(args)
    for item_type in item_type_routes:
        request_string = 'https://poe.ninja/api/data/itemoverview?league={league}&type={type}'.format(league=current_league, type=item_type)
        r = requests.get(request_string)
        if item_type in ['UniqueWeapon', 'UniqueArmour']:  # items that have different price per links
            if requested_item[-2:] in ['0L', '0l', '5L', '5l', '6l', '6L']:  # checking for specific linkage (0,5,6)
                links = requested_item[-2:]  # last two chars are the num links
                requested_item_name = requested_item[:-3]  # strip the num links and whitespace
                for item in r.json()['lines']:
                    if (item['name'].replace("'", '').lower() in [requested_item_name, requested_item_name.replace("'", '').lower()]) and str(item['links']) == str(requested_item[-2]):
                        return_statement = 'A {arg1} linked {arg2} is currently worth {arg3} exalted orbs.'.format(arg1=str(item['links']), arg2=item['name'], arg3=str(item['exaltedValue']))
                        return await ctx.send(return_statement)

            else:  # if no listed links, assume 0 links
                for item in r.json()['lines']:
                    if (item['name'].replace("'", '').lower() in [requested_item, requested_item.replace("'", '').lower()]) and str(item['links']) == str(0):
                        return_statement = 'A {arg1} linked {arg2} is currently worth {arg3} exalted orbs.'.format(arg1=str(item['links']), arg2=item['name'], arg3=str(item['exaltedValue']))
                        return await ctx.send(return_statement)

        else:  # otherwise, links don't matter
            for item in r.json()['lines']:
                if item['name'].replace("'", '').lower() in [requested_item, requested_item.replace("'", '').lower()]:
                    return_statement = '{item} is currently worth {price} exalted orbs.'.format(item=item['name'], price=str(item['exaltedValue']))
                    return await ctx.send(return_statement)


    return_statement = 'Cannot find: {item}. \nPlease make sure that you are typing the full name of the item.'.format(item=requested_item)
    await ctx.send(return_statement)


@bot.command(name='exalt')
async def exalt(ctx):
    """
    Displays the current chaos value for a single exalt
    :param ctx:
    :return: Returns string with chaos value of single exalt
    """
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league={league}&type=Currency&language=en'.format(league=current_league)
    r = requests.get(request_string)
    for currency in r.json()['lines']:
        if currency['currencyTypeName'] == 'Exalted Orb':
            returnStatement = '{curr}s are currently worth {chaos} chaos orbs.'.format(curr=currency['currencyTypeName'], chaos=str(currency['chaosEquivalent']))
    await ctx.send(returnStatement)


@bot.command(name='c', aliases=['chaos'])
async def chaosEquivalent(ctx, *args):
    """
    Displays the chaos equivalent of any items with "currency" tag
    :param ctx:
    :param args: item with "currency" tag (e.g. Orb of Transmutation)
    :return: Returns string with chaos value of requested currency
    """
    requested_currency = ' '.join(args)
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league={league}&type=Currency&language=en'.format(league=current_league)
    r = requests.get(request_string)
    currency_dict = {}  # dict format -- name: [correct name: chaos equivalent]
    simplified_user_request = requested_currency.replace("'", '').lower()

    for currency in r.json()['lines']:
        simplified_name = currency['currencyTypeName'].replace("'", '').lower()  # remove apostrophe and lowercase
        price = [currency['currencyTypeName'], str(currency['chaosEquivalent'])]
        currency_dict[simplified_name] = price
    try:
        return_statement = "{arg1}\'s are worth **{arg2}** chaos orbs.".format(arg1=currency_dict[simplified_user_request][0], arg2=currency_dict[simplified_user_request][1])
        await ctx.send(return_statement)
    except:
        return_statement = 'Cannot find: {curr}. \nPlease make sure that you are typing the full name of the currency.'.format(curr=requested_currency)
        await ctx.send(return_statement)


@bot.command(name='e', aliases=['ex'])
async def exaltEquivalent(ctx, *args):
    """
    Displays the exalt equivalent of any items with "currency" tag
    :param ctx:
    :param args: item with "currency" tag (e.g. Orb of Transmutation)
    :return: Return string with exalt value of requested currency
    """
    requested_currency = ' '.join(args)
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league={league}&type=Currency&language=en'.format(league=current_league)
    r = requests.get(request_string)
    simplified_user_request = requested_currency.replace("'", '').lower()
    for currency in r.json()['lines']:
        if currency['currencyTypeName'] == 'Exalted Orb':
            exalt_value = currency['chaosEquivalent']
            break

    currency_dict = {}  # dict format -- {simplified name: [correct name: exalt equivalent]}
    for currency in r.json()['lines']:
        simplified_currency = currency['currencyTypeName'].replace("'", '').lower()  # remove apostrophe and lowercase
        currency_dict[simplified_currency] = [currency['currencyTypeName'], str(round(currency['chaosEquivalent'] / exalt_value, 2))]
    try:
        return_statement = "{arg1}\'s are worth **{arg2}** exalted orbs.".format(arg1=currency_dict[simplified_user_request][0], arg2=currency_dict[simplified_user_request][1])
        await ctx.send(return_statement)
    except:  # make less broad
        return_statement = 'Cannot find: {curr}. \nPlease make sure that you are typing the full name of the currency.'.format(curr=requested_currency)
        await ctx.send(return_statement)


@bot.command(name='ec', aliases=['ce'])
async def exaltChaosEquivalent(ctx, *args):
    """
    Displays the exalt and chaos remainder equivalent of any items with "currency" tag
    :param ctx:
    :param args: item with "currency" tag (e.g. Mirror Shard)
    :return: Return string with exalt and chaos value of requested currency
    """
    requested_currency = ' '.join(args)
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league={league}&type=Currency&language=en'.format(league=current_league)
    r = requests.get(request_string)

    for currency in r.json()['lines']:
        if currency['currencyTypeName'] == 'Exalted Orb':
            exalt_value = currency['chaosEquivalent']
            break

    currency_dict = {}  # dict format -- {name: [correct name, exalt quotient, chaos remainder]}
    for currency in r.json()['lines']:
        simplified_name = currency['currencyTypeName'].replace("'", '').lower()  # remove apostrophe and lowercase
        currency_dict[simplified_name] = [currency['currencyTypeName'], str(currency['chaosEquivalent'] // exalt_value), str(round(currency['chaosEquivalent'] % exalt_value))]
        currency_dict[currency['currencyTypeName']] = [currency['currencyTypeName'], str(currency['chaosEquivalent'] // exalt_value), str(round(currency['chaosEquivalent'] % exalt_value))]
    try:
        return_statement = "{arg1}\'s are worth a total of **{arg2}** exalted orbs and {arg3} chaos orbs.".format(arg1=currency_dict[requested_currency][0], arg2=currency_dict[requested_currency][1], arg3=currency_dict[requested_currency][2])
        await ctx.send(return_statement)
    except:  # make less broad
        return_statement = 'Cannot find: {curr}. \nPlease make sure that you are typing the full name of the currency'.format(curr=requested_currency)
        await ctx.send(return_statement)


@bot.command(name='!positions')
async def positions(ctx):  # portfolio
    """
    Displays a table of current stock holdings
    :param ctx:
    :return: Return string with multiple lines of stocks
    """
    my_stocks = robin_stocks.build_holdings()
    positions = ''
    for key, value in my_stocks.items():
        positions += ''.join(('{key}, Price: {price}, Quantity: {quantity}\n'.format(key=key, price=str(round(float(value['price']), 2)), quantity=str(round(float(value['quantity']))))))
    await ctx.send(positions)


@bot.command(name='random')
async def positions(ctx, *args):
    if len(args) != 2:
        await ctx.send('must be two numbers dummy')
    else:
        random_num = random.randrange(int(args[0]), int(args[1]))
        await ctx.send(random_num)


@bot.command(name='hello', aliases=['Hello', 'Hi', 'hi'])
async def hello(ctx):
    await ctx.send('Hello, {name}'.format(name=ctx.message.author.name))


@bot.command(name='choke')
async def choke(ctx):
    await ctx.send(file=discord.File('richardpics/richardchoke.jpg'))


@bot.command(name='whoisright')
async def whoisright(ctx):
    await ctx.send(file=discord.File('richardpics/fiddle.jpg'))


@bot.command(name='richardree')
async def richardree(ctx):
    await ctx.send(file=discord.File('richardpics/richardgasm.jpg'))


@bot.command(name='swagswagbitch')
async def richardree(ctx):
    await ctx.send(file=discord.File('richardpics/richard9.jpg'))


@bot.command(name='gunmo')
async def gunmo(ctx):
    response = ('<@{num}>\n'.format(num=str(121871886673117184)))
    await ctx.send(response)


@bot.command(name='!richard')
async def randomRichard(ctx):
    await ctx.send(file=discord.File(random.choice(richardPics)))


@bot.command(name='poggers')
async def ryanO(ctx):
    await ctx.send(file=discord.File('images/ryanO.png'))


@bot.command(name='jimothy')
async def jimothy(ctx):
    await ctx.send(file=discord.File('images/jimothy.png'))


@bot.command(name='burger')
async def burger(ctx):
    await ctx.send(file=discord.File('images/burger.jpg'))


@bot.command(name='sike')
async def sike(ctx):
    await ctx.send(file=discord.File('images/sike.png'))


@bot.command(name='!question')
async def interviewquestion(ctx):
    await ctx.send(random.choice(interviewQuestions))


@bot.command(name='commit')
async def death(ctx, arg):
    """
    Ends program if user is authorized
    :param ctx:
    :param arg: must equal "death"
    :return: n/a
    """
    authorized = [142739501557481472]
    if arg == 'die' and ctx.message.author.id in authorized:
        await ctx.send('u have killed me')
        sys.exit(0)
    else:
        await ctx.send('woosh u missed')


@bot.command(name='id')
async def identify(ctx, *args):
    requested_item = ' '.join(arg.capitalize() for arg in args)
    found_item = find(requested_item)
    if found_item:  # todo: create embed class/ embed function depending on item type
        e = create_poe_item_embed(found_item)
        await ctx.send(embed=e)
    else:
        await ctx.send('{item} was not found. Please @ADKarry if you think this is an error.'.format(item=requested_item))


@bot.command(name='calc')
async def calc(ctx, arg):
    try:
        await ctx.send(Calc.evaluate(arg))
    except Exception as err:
        await ctx.send(err)


@bot.command(name="z")
async def countdown_90(ctx):
    resting = True
    i = 90
    while resting and i > 0:
        if i >= 15 and i % 15 == 0:
            await ctx.send(i)
        elif i < 15:
            await ctx.send(i)
        i -= 1
        time.sleep(1)
    await ctx.send("sadge")


@bot.command(name="x")
async def countdown_60(ctx):
    resting = True
    i = 60
    while resting and i > 0:
        if i >= 15 and i % 15 == 0:
            await ctx.send(i)
        elif i < 15:
            await ctx.send(i)
        i -= 1
        time.sleep(1)
    await ctx.send("sadge")

print("janbot running...")
bot.run(token)
