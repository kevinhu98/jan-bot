# bot.py
import os
import discord
import robin_stocks
import requests
from discord.ext import commands
from dotenv import load_dotenv
import praw
import glob
import random
import sys
import pymongo
load_dotenv()


# setting up discord api info
token = os.getenv('DISCORD_TOKEN')


# setting up robinhood api info
login = robin_stocks.login(os.getenv('ROBINHOOD_LOGIN'),os.getenv('ROBINHOOD_PW'))


# setting up richard image paths
richardPicDir = glob.glob("richardpics/*")
richardPics = []
for path in richardPicDir:
    richardPics.append(path.replace("\\", "/"))


# setting up interview questions
with open("text_file_resources/interviewquestions.txt") as f:
    interviewQuestions = [question for question in f]


# setting up poe ninja routes and league info
current_league = "Ritual"
item_type_routes = ["UniqueWeapon", "DivinationCard", "UniqueArmour", "UniqueAccessory", "UniqueJewel", "UniqueFlask", "UniqueMap",
                    "Oil", "Incubator", "Scarab", "SkillGem", "Fossil", "Resonator", "Prophecy", "Beast", "Essence"]


currency_type_routes = ["Currency", "Fragment"]

# setting up a read-only reddit instance
reddit = praw.Reddit(
     client_id= os.getenv('REDDIT_CLIENT_ID'),
     client_secret= os.getenv('REDDIT_CLIENT_SECRET'),
     user_agent="my user agent"
)

# connect to db

try:
    client = pymongo.MongoClient("mongodb+srv://kevin:" + os.getenv('MONGO_PW') + "@cluster0.8xh0x.mongodb.net/poe.users?retryWrites=true&w=majority")
    poe_client = client.poe
    poe_users = poe_client.users
    print('Successful connection')
except:
    print('no connection')


bot = commands.Bot(command_prefix='', help_command=None)

#to do: auto update current_league, update and move to different modules?

@bot.command(name="help")
async def help(ctx):
    """
    Displays a discord embed object with a list of commands
    :param ctx:
    :return: Prints an embed object
    """
    embedVar = discord.Embed(title="Janbot Commands", description="look at that boy go", color=0xff0000)
    embedVar.add_field(name="c 'currency'", value="Returns the chaos orb equivalent of currency", inline=False)
    embedVar.add_field(name="e 'currency'", value="Returns the exalted orb equivalent of currency", inline=False)
    embedVar.add_field(name="ce 'currency'", value="Returns the total exalted and chaos orb equivalent of currency", inline=False)
    embedVar.add_field(name="ci 'item' 'optional: 0l,5l,6l'", value="Returns the chaos orb equivalent of item", inline=False)
    embedVar.add_field(name="ei 'item'", value="Returns the exalted orb equivalent of item", inline=False)
    embedVar.add_field(name="!stonks", value="Displays portfolio value", inline=False)
    embedVar.add_field(name="!positions", value="Displays account positions", inline=False)
    embedVar.add_field(name="!richard", value="Random richard picture", inline=False)
    await ctx.send(embed=embedVar)

@bot.command(name="ci")
async def item_chaos_price(ctx, *args):
    """
    Given any item, displays the chaos value of object
    :param ctx:
    :param args: first argument is the name of the item, second optional argument is number of links if possible
    :return: Returns string with chaos value
    """
    requested_item = " ".join(args)

    for item_type in item_type_routes:
        request_string = 'https://poe.ninja/api/data/itemoverview?league={}&type={}'.format(current_league, item_type)
        r = requests.get(request_string)
        if item_type in ["UniqueWeapon", "UniqueArmour"]:  # items that have different price per links
            if requested_item[-2:] in ["0L", "0l", "5L", "5l", "6l", "6L"]:  # checking for specific linkage (0,5,6)
                links = requested_item[-2:]  # last two chars are the num links
                requested_item_name = requested_item[:-3]  # strip the num links and whitespace
                for item in r.json()['lines']:
                    if (item['name'].replace("'", "").lower() in [requested_item_name, requested_item_name.replace("'", "").lower()]) and str(item['links']) == str(requested_item[-2]):
                        return_statement = "A " + str(item['links']) + " linked " + item['name'] + ' is currently worth ' + str(item['chaosValue']) + " chaos orbs."
                        await ctx.send(return_statement)
                        return
            else:  # if no listed links, assume 0 links
                for item in r.json()['lines']:
                    if (item['name'].replace("'", "").lower() in [requested_item, requested_item.replace("'","").lower()]) and str(item['links']) == str(0):
                        return_statement = "A " + str(item['links']) + " linked " + item['name'] + ' is currently worth ' + str(item['chaosValue']) + " chaos orbs."
                        await ctx.send(return_statement)
                        return
        else:  # otherwise, links don't matter
            for item in r.json()['lines']:
                if item['name'].replace("'", "").lower() in [requested_item, requested_item.replace("'", "").lower()]:
                    return_statement = item['name'] + ' is currently worth ' + str(item['chaosValue']) + " chaos orbs."
                    await ctx.send(return_statement)
                    return

    for currency_type in currency_type_routes:
        request_string = 'https://poe.ninja/api/data/currencyoverview?league={}&type={}'.format(current_league, currency_type)
        r = requests.get(request_string)
        for item in r.json()['lines']:
            if item['currencyTypeName'].replace("'", "").lower() in [requested_item, requested_item.replace("'", "").lower()]:
                return_statement = item['currencyTypeName'] + ' is currently worth ' + str(item['chaosEquivalent']) + " chaos orbs."
                await ctx.send(return_statement)
                return

    return_statement = "Cannot find: " + requested_item + ". \n" + "Please make sure that you are typing the full name of the item."
    await ctx.send(return_statement)

@bot.command(name="ei")
async def item_exalt_price(ctx, *args):
    """
    Given any item, displays the exalt value of object
    :param ctx:
    :param args: first argument is the name of the item, second optional argument is number of links if possible
    :return: Returns string with exalt value
    """
    requested_item = " ".join(args)
    for item_type in item_type_routes:
        request_string = 'https://poe.ninja/api/data/itemoverview?league={}&type={}'.format(current_league, item_type)
        r = requests.get(request_string)
        if item_type in ["UniqueWeapon", "UniqueArmour"]:  # items that have different price per links
            if requested_item[-2:] in ["0L", "0l", "5L", "5l", "6l", "6L"]:  # checking for specific linkage (0,5,6)
                links = requested_item[-2:]  # last two chars are the num links
                requested_item_name = requested_item[:-3]  # strip the num links and whitespace
                for item in r.json()['lines']:
                    if (item['name'].replace("'", "").lower() in [requested_item_name, requested_item_name.replace("'", "").lower()]) and str(item['links']) == str(requested_item[-2]):
                        return_statement = "A " + str(item['links']) + " linked " + item['name'] + ' is currently worth ' + str(item['exaltedValue']) + " exalted orbs."
                        await ctx.send(return_statement)
                        return
            else:  # if no listed links, assume 0 links
                for item in r.json()['lines']:
                    if (item['name'].replace("'", "").lower() in [requested_item, requested_item.replace("'", "").lower()]) and str(item['links']) == str(0):
                        return_statement = "A " + str(item['links']) + " linked " + item['name'] + ' is currently worth ' + str(item['exaltedValue']) + " exalted orbs."
                        await ctx.send(return_statement)
                        return
        else:  # otherwise, links don't matter
            for item in r.json()['lines']:
                if item['name'].replace("'", "").lower() in [requested_item, requested_item.replace("'", "").lower()]:
                    return_statement = item['name'] + ' is currently worth ' + str(item['exaltedValue']) + " exalted orbs."
                    await ctx.send(return_statement)
                    return

    return_statement = "Cannot find: " + requested_item + ". \n" + "Please make sure that you are typing the full name of the item."
    await ctx.send(return_statement)


@bot.command(name="exalt")
async def exalt(ctx):
    """
    Displays the current chaos value for a single exalt
    :param ctx:
    :return: Returns string with chaos value of single exalt
    """
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league={}&type=Currency&language=en'.format(current_league)
    r = requests.get(request_string)
    for currency in r.json()['lines']:
        if currency['currencyTypeName'] == "Exalted Orb":
            returnStatement = currency['currencyTypeName'] +'s' + ' are currently worth ' + str(currency['chaosEquivalent']) + " chaos orbs."
    await ctx.send(returnStatement)


@bot.command(name="c", aliases=["chaos"])
async def chaosEquivalent(ctx, *args):
    """
    Displays the chaos equivalent of any items with "currency" tag
    :param ctx:
    :param args: item with "currency" tag (e.g. Orb of Transmutation)
    :return: Returns string with chaos value of requested currency
    """
    requested_currency = " ".join(args)
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league={}&type=Currency&language=en'.format(current_league)
    r = requests.get(request_string)
    currency_dict = {}  # dict format -- name: [correct name: chaos equivalent]
    simplified_user_request = requested_currency.replace("'", "").lower()

    for currency in r.json()['lines']:
        simplified_name = currency['currencyTypeName'].replace("'", "").lower()  # remove apostrophe and lowercase
        price = [currency['currencyTypeName'], str(currency['chaosEquivalent'])]
        currency_dict[simplified_name] = price
    try:
        return_statement = currency_dict[simplified_user_request][0] + '\'s' + " are worth " + "**" + currency_dict[simplified_user_request][1] + "**" + " chaos orbs."
        await ctx.send(return_statement)
    except:
        return_statement = "Cannot find: " + requested_currency + ". \n" + "Please make sure that you are typing the full name of the currency."
        await ctx.send(return_statement)


@bot.command(name="e")
async def exaltEquivalent(ctx, *args):
    """
    Displays the exalt equivalent of any items with "currency" tag
    :param ctx:
    :param args: item with "currency" tag (e.g. Orb of Transmutation)
    :return: Return string with exalt value of requested currency
    """
    requested_currency = " ".join(args)
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league={}&type=Currency&language=en'.format(current_league)
    r = requests.get(request_string)
    simplified_user_request = requested_currency.replace("'", "").lower()
    for currency in r.json()['lines']:
        if currency['currencyTypeName'] == "Exalted Orb":
            exalt_value = currency['chaosEquivalent']
            break

    currency_dict = {}  # dict format -- {simplified name: [correct name: exalt equivalent]}
    for currency in r.json()['lines']:
        simplified_currency = currency['currencyTypeName'].replace("'", "").lower()  # remove apostrophe and lowercase
        currency_dict[simplified_currency] = [currency['currencyTypeName'], str(round(currency['chaosEquivalent'] / exalt_value, 2))]
    try:
        return_statement = currency_dict[simplified_user_request][0] + '\'s' + " are worth " + "**" + currency_dict[simplified_user_request][1] + "**" + " exalted orbs."
        await ctx.send(return_statement)
    except:  # make less broad
        return_statement = "Cannot find: " + requested_currency + ". \n" + "Please make sure that you are typing the full name of the currency."
        await ctx.send(return_statement)


@bot.command(name="ec", aliases=["ce"])
async def exaltChaosEquivalent(ctx, *args):
    """
    Displays the exalt and chaos remainder equivalent of any items with "currency" tag
    :param ctx:
    :param args: item with "currency" tag (e.g. Mirror Shard)
    :return: Return string with exalt and chaos value of requested currency
    """
    requested_currency = " ".join(args)
    request_string = 'https://poe.ninja/api/data/CurrencyOverview?league={}&type=Currency&language=en'.format(current_league)
    r = requests.get(request_string)

    for currency in r.json()['lines']:
        if currency['currencyTypeName'] == "Exalted Orb":
            exalt_value = currency['chaosEquivalent']
            break

    currency_dict = {}  # dict format -- {name: [correct name, exalt quotient, chaos remainder]}
    for currency in r.json()['lines']:
        simplified_name = currency['currencyTypeName'].replace("'", "").lower()  # remove apostrophe and lowercase
        currency_dict[simplified_name] = [currency['currencyTypeName'], str(currency['chaosEquivalent'] // exalt_value), str(round(currency['chaosEquivalent'] % exalt_value))]
        currency_dict[currency['currencyTypeName']] = [currency['currencyTypeName'], str(currency['chaosEquivalent'] // exalt_value), str(round(currency['chaosEquivalent'] % exalt_value))]
    try:
        return_statement = currency_dict[requested_currency][0] + '\'s' + " are worth a total of " + \
                           "**" + currency_dict[requested_currency][1] + "**" + " exalted orbs and " + currency_dict[requested_currency][2] + " chaos orbs."
        await ctx.send(return_statement)
    except:  # make less broad
        return_statement = "Cannot find: " + requested_currency + ". \n" + "Please make sure that you are typing the full name of the currency."
        await ctx.send(return_statement)


@bot.command(name="!positions")
async def positions(ctx):  # portfolio
    """
    Displays a table of current stock holdings
    :param ctx:
    :return: Return string with multiple lines of stocks
    """
    my_stocks = robin_stocks.build_holdings()
    positions = ""
    for key, value in my_stocks.items():
        positions += "".join((key + ", " + "Price: " + str(round(float(value["price"]), 2)) + "," + " Quantity: " + str(round(float(value["quantity"]))))) + "\n"
    await ctx.send(positions)


@bot.command(name="!stonks")
async def stonks(ctx):
    """
    Displays current account portfolio
    :param ctx:
    :return: Return string with amount in robinhood account
    """
    await ctx.send(robin_stocks.profiles.load_portfolio_profile(info="equity"))


@bot.command(name="random")
async def positions(ctx, *args):
    if len(args) != 2:
        await ctx.send('must be two numbers dummy')
    else:
        random_num = random.randrange(int(args[0]), int(args[1]))
        await ctx.send(random_num)


@bot.command(name="hello", aliases=["Hello", "Hi", "hi"])
async def hello(ctx):
    return_string = "Hello, " + ctx.message.author.name
    await ctx.send(return_string)


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


@bot.command(name="richard")
async def randomRichard(ctx):
    await ctx.send(file=discord.File(random.choice(richardPics)))


@bot.command(name="poggers")
async def ryanO(ctx):
    await ctx.send(file=discord.File('images/ryanO.png'))


@bot.command(name="jimothy")
async def jimothy(ctx):
    await ctx.send(file=discord.File('images/jimothy.png'))


@bot.command(name="burger")
async def burger(ctx):
    await ctx.send(file=discord.File('images/burger.jpg'))


@bot.command(name="sike")
async def sike(ctx):
    await ctx.send(file=discord.File('images/sike.png'))


@bot.command(name="!question")
async def interviewquestion(ctx):
    await ctx.send(random.choice(interviewQuestions))


'''  
@bot.command(name="wsb")  
# apparently this already exists
async def positions(ctx):
    post_number = 1
    limit = 20
    await ctx.send("Here are the top {} hot posts on wsb:".format(limit))
    for submission in reddit.subreddit("wallstreetbets").hot(limit=limit):
        post_number_return_string = "The current post number: " + str(post_number_return_string)
        await ctx.send()
        for top_level_comment in submission.comments:
            try:
                return_statement = top_level_comment.body + str(top_level_comment.score)
                await ctx.send(return_statement)
            except discord.errors.HTTPException:  # body length too long
                await ctx.send("2000 length")
'''


@bot.command(name="commit")
async def death(ctx, arg):
    """
    Ends program if user is authorized
    :param ctx:
    :param arg: must equal "death"
    :return: n/a
    """
    authorized = [142739501557481472]
    if arg == "die" and ctx.message.author.id in authorized:
        await ctx.send("u have killed me")
        sys.exit(0)
    else:
        await ctx.send("woosh u missed")

@bot.command(name="!register")
async def register(ctx):
    requestor_id = ctx.message.author.id
    if poe_users.find_one({"id": requestor_id}):
        registered_string = ctx.message.author.name + " is already registered"
        await ctx.send(registered_string)
    else:
        user_to_register = {"id": requestor_id, "items": []}
        poe_users.insert_one(user_to_register)
        register_string = ctx.message.author.name + " is now registered"
        await ctx.send(register_string)
        print("user has been registered")

'''
# WIP
@bot.command(name="!add")
async def add(ctx, *args):
    requestor_id = ctx.message.author.id
    if not poe_users.find_one({"id": requestor_id}):
        not_registered_string = "You are not currently registered. You can register using **!register**."
        await ctx.send(not_registered_string)
    else:

@bot.command(name="id")
async def id(ctx):
'''

@bot.command(name="id")  #todo : div cards such as "A Dab of Ink are not found"
async def id(ctx, *args):
    requested_item = " ".join(arg.capitalize() for arg in args)  #todo : all words should not be capitalized, or do a regex
    item_collections = poe_client.list_collection_names()
    item_collections.remove("currencies")
    item_collections.remove("users")

    is_item_found = False
    for collection_name in item_collections:
        specific_type_collection = poe_client.get_collection(collection_name)
        if (specific_type_collection.find_one({"name": requested_item})):
            is_item_found = True
            found_item = specific_type_collection.find_one({"name": requested_item})
            found_item = dict(found_item)
            break

    if is_item_found:
        embedVar = discord.Embed(title=found_item['name'], url=found_item['url'], description="uwu", color=0xff0000)  # todo: update color based on item type and extra fields based on type
        embedVar.set_thumbnail(url=found_item['icon'])
        embedVar.add_field(name="Level Required: ", value=found_item['levelRequired'], inline=False)
        for modifier in found_item['implicitModifiers']:
            embedVar.add_field(name="Explicit: ", value=modifier)
        for modifier in found_item['explicitModifiers']:
            embedVar.add_field(name="Implicit: ", value=modifier)
        await ctx.send(embed=embedVar)

    else:
        not_found_response = requested_item + " was not found. Please @ADKarry if you think this is an error."
        await ctx.send(not_found_response)
bot.run(token)