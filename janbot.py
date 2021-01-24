# bot.py
import os
import discord
import robin_stocks
import requests
import re
from discord.ext import commands
from dotenv import load_dotenv

import glob
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

login = robin_stocks.login(os.getenv('ROBINHOOD_LOGIN'),os.getenv('ROBINHOOD_PW'))


bot = commands.Bot(command_prefix='')

richardPicDir = glob.glob("richardpics/*")
richardPics = []

with open("interviewquestions.txt") as f:
    interviewQuestions = [question for question in f]

for path in richardPicDir:
    richardPics.append(path.replace("\\", "/"))

@bot.command(name="chaos")
async def chaos(ctx):
    await ctx.send("Chaos Orbs are worth 1 chaos orbs.")

@bot.command(name="exalt")
async def exalt(ctx):
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league=Ritual&type=Currency&language=en'
    r = requests.get(request_string)
    for currency in r.json()['lines']:
        if currency['currencyTypeName'] == "Exalted Orb":
            returnStatement = currency['currencyTypeName'] +'s' + ' are currently worth ' + str(currency['chaosEquivalent']) + " chaos orbs."
    await ctx.send(returnStatement)

@bot.command(name="c")
async def chaosEquivalent(ctx, *args):
    requested_currency = " ".join(args)
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league=Ritual&type=Currency&language=en'
    r = requests.get(request_string)
    currency_dict = {}  # dict format -- name: [correct name: chaos equivalent]
    for currency in r.json()['lines']:
        simplified_name = currency['currencyTypeName'].replace("'", "").lower()  # remove apostrophe and lowercase
        currency_dict[simplified_name] = [currency['currencyTypeName'], str(currency['chaosEquivalent'])]
        currency_dict[currency['currencyTypeName']] = str(currency['chaosEquivalent'])

    try:
        return_statement = currency_dict[requested_currency][0] + '\'s' + " are worth " + "**" + currency_dict[requested_currency][1] + "**" + " chaos orbs."
        await ctx.send(return_statement)
    except:
        return_statement = "Cannot find: " + requested_currency + ". \n" + "Please make sure that you are typing the full name of the currency."
        await ctx.send(return_statement)

@bot.command(name="bf")  # bottled faith
async def bf(ctx):
    request_string = 'https://poe.ninja/api/data/ItemOverview?league=Ritual&type=UniqueFlask&language=en'
    r = requests.get(request_string)
    for item in r.json()['lines']:
        if item['name'] == "Bottled Faith":
            returnStatement = item['name'] + 's' + ' are currently worth ' + str(item['chaosValue'] + " chaos orbs.")
    await ctx.send(returnStatement)
'''
@bot.command(name="currency")
async def currency(ctx):
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league=Ritual&type=Currency&language=en'
    r = requests.get(request_string)
    returnStatement = ""
    for currency in r.json()['lines']:
        returnStatement = currency['currencyTypeName'] +'s' + ' are currently worth ' + str(currency['chaosEquivalent']) + " chaos orbs."
        await ctx.send(returnStatement)
'''

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("im janbot")

@bot.command(name="choke")
async def choke(ctx):
    await ctx.send(file=discord.File('richardpics/richardchoke.jpg'))

@bot.command(name="whoisright")
async def whoisright(ctx):
    await ctx.send(file=discord.File('richardpics/fiddle.jpg'))

@bot.command(name="richardree")
async def richardree(ctx):
    await ctx.send(file=discord.File('richardpics/richardgasm.jpg'))

@bot.command(name="swagswagbitch")
async def richardree(ctx):
    await ctx.send(file=discord.File('richardpics/richard9.jpg'))

@bot.command(name='gunmo')
async def gunmo(ctx):

    response = ("<@" + str(121871886673117184) + ">" + "\n")

    await ctx.send(response)

@bot.command(name="!richard")
async def randomRichard(ctx):
    await ctx.send(file=discord.File(random.choice(richardPics)))

@bot.command(name="poggers")
async def ryanO(ctx):
    await ctx.send(file=discord.File('images/ryanO.png'))

@bot.command(name="!jimothy")
async def jimothy(ctx):
    await ctx.send(file=discord.File('images/jimothy.png'))

@bot.command(name="!burger")
async def burger(ctx):
    await ctx.send(file=discord.File('images/burger.jpg'))

@bot.command(name="sike")
async def sike(ctx):
    await ctx.send(file=discord.File('images/sike.png'))

@bot.command(name="!question")
async def interviewquestion(ctx):
    await ctx.send(random.choice(interviewQuestions))

@bot.command(name="!stonks")
async def stonks(ctx):  # portfolio
    await ctx.send(robin_stocks.profiles.load_portfolio_profile(info="equity"))

@bot.command(name="!positions")
async def positions(ctx):  # portfolio
    my_stocks = robin_stocks.build_holdings()
    positions = ""
    for key, value in my_stocks.items():
        positions += "".join((key + ", " + "Price: " + str(round(float(value["price"]), 2)) + "," + " Quantity: " + str(round(float(value["quantity"]))))) + "\n"
    await ctx.send(positions)

bot.run(token)