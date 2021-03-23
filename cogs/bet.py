from discord.ext import commands
from ext.setup import *
from bson.objectid import ObjectId

class Bet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bets = connectToBetDB().bet

    @commands.command(name='$bethelp')
    async def displayBetHelp(self, ctx):
        await ctx.send("$bet Betting Against, Team 1, Team 2, Prediction, Odds, Amount")
        await ctx.send("Example: $bet ADKarry, TSM, TL, TL, 1:2, 20")

    @commands.command(name='$bet')
    async def createBet(self, ctx, *args):
        requester_id = ctx.message.author.id
        betParams = ''.join(args).split(",")
        if len(betParams) < 6:
            await ctx.send("Missing a parameter")
            return
        elif len(betParams) > 6:
            await ctx.send("Too many parameters")
            return
        betRatio = float(betParams[4].split(":")[1])/float(betParams[4].split(":")[0])
        betting_against_amount = float(betParams[5]) * betRatio

        bet_to_create = {'created_by': requester_id,
                         'betting_against': betParams[0],
                         'team_1': betParams[1],
                         'team_2': betParams[2],
                         'created_by_prediction': betParams[3],
                         'odds': betParams[4],
                         'amount': betParams[5],
                         'betting_against_amount': betting_against_amount,  # amount other person is betting
                         'accepted': False,
                         'winner': None
                         }
        bet_object = self.bets.insert_one(bet_to_create)
        await ctx.send("Bet created, id: {bet_id}".format(bet_id=bet_object.inserted_id))

    @commands.command(name='$accept')
    async def updateAcceptedStatus(self, ctx, arg):
        self.bets.find_one_and_update(
            {"_id": ObjectId(arg)},
            {"$set": {"accepted": True}})
        await ctx.send(self.bets.find_one({"_id": ObjectId(arg)}))
        #self.bets.find_one_and_update()


    @commands.command(name='$active')
    async def listActive(self, ctx):
        requester_id = ctx.message.author.id
        cur = self.bets.find({
            "created_by": requester_id,
            "accepted": True
        })
        for doc in cur:
            await ctx.send(doc)
       # await ctx.send()