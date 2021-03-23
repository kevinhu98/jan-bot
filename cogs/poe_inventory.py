from discord.ext import commands
from ext.utilities import *
from price_check import *
from ext.setup import *

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = connectToPoeDB().users

    def find_user(self, discord_id):
        return self.users.find_one({"id": discord_id})

    @commands.command(name='!register')
    async def register(self, ctx):
        requester_id = ctx.message.author.id
        if self.users.find_one({'id': requester_id}):
            registered_string = '{name} is already registered'.format(name=ctx.message.author.name)
            await ctx.send(registered_string)
        else:
            user_to_register = {'id': requester_id, 'items': []}
            self.users.insert_one(user_to_register)
            register_string = '{name} is now registered'.format(name=ctx.message.author.name)
            await ctx.send(register_string)

    @commands.command(name='!add')
    async def add(self, ctx, *args):  # check registered, check item exists, check user has item already
        requester = self.find_user(ctx.message.author.id)  # single user document
        requested_item = " ".join(args)
        item_to_find = find(requested_item)  # check item does exist and return item object

        if not requester:
            await ctx.send("You are not currently registered. You can register using **!register**.")
        elif not item_to_find:
            await ctx.send("Item does not exist.")
        elif item_to_find['name'] in requester['items']:
            await ctx.send("This item is already on your list.")
        else:
            self.users.find_one_and_update(
                {"id": requester['id']},
                {"$push": {"items": item_to_find["name"]},
                 })
            await ctx.send('{item} has now been added to your list.'.format(item=item_to_find["name"]))

    @commands.command(name='!remove')
    async def remove(self, ctx, *args):  # check registered, check item exists, check user has item already
        requester = self.find_user(ctx.message.author.id)  # single user document
        requested_item = " ".join(args)
        item_to_find = find(requested_item)  # check item does exist and return item object

        if not requester:
            await ctx.send("You are not currently registered. You can register using **!register**.")
        elif not item_to_find:
            await ctx.send("Item does not exist.")
        else:
            self.users.find_one_and_update(
                {"id": requester['id']},
                {"$pull": {"items": item_to_find["name"]},
                 })
            await ctx.send('{item} has now been removed from your list.'.format(item=item_to_find["name"]))

    @commands.command(name='!list')
    async def list_items(self, ctx):
        requester = self.find_user(ctx.message.author.id)  # single user document
        if not requester:
            await ctx.send("You are not currently registered. You can register using **!register**.")
        elif not requester['items']:
            await ctx.send("You currently have no items on your list")
        else:
            await ctx.send("Here are the items you have on your list:")
            for i, item in enumerate(requester['items'], 1):
                await ctx.send('{num}. {item}'.format(num=i, item=item))

    @commands.command(name="!pricecheck")
    async def price_check(self, ctx):
        requester = self.find_user(ctx.message.author.id)
        for item in requester['items']:
            await ctx.send(price_check(item))
