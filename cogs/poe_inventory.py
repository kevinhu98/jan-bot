from discord.ext import commands
from ext.utilities import *


class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = connectToDB().users

    # todo: write separate function, checking if user is registered

    @commands.command(name='!add')
    async def add(self, ctx, *args):  # check registered, check item exists, check user has item already
        # todo: first check registered

        requester_id = ctx.message.author.id  # discord id
        requester = self.users.find_one({"id": requester_id})  # single requester document
        requested_item = " ".join(args)
        item_to_find = find(requested_item.capitalize())  # check item does exist and return item object
        # todo: fix this cursed code block
        # check if item already exists in user list
        if not requester:
            await ctx.send("You are not currently registered. You can register using **!register**.")
        elif not item_to_find:
            await ctx.send("Item does not exist.")
        elif self.users.find_one({"id": requester_id, "items": {"$in": [item_to_find["name"]]}}):
            await ctx.send("This item is already on your list.")
        else:
            self.users.find_one_and_update(
                {"id": requester_id},
                {"$push": {"items": item_to_find["name"]},
                 })
            return_string = item_to_find["name"] + " has now been added to your list."
            await ctx.send(return_string)

    @commands.command(name='!list')
    async def list_items(self, ctx):
        # todo: first check registered

        requester_id = ctx.message.author.id  # discord id
        requester = self.users.find_one({"id": requester_id})  # single requester document
        if not requester['items']:
            await ctx.send("You currently have no items on your list")
        else:
            await ctx.send("Here are the items you have on your list:")
            for i, item in enumerate(requester['items'], 1):
                await ctx.send('{}. {}'.format(i, item))
