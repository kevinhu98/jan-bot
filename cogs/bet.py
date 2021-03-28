from discord.ext import commands
from ext.setup import *
from bson.objectid import ObjectId
from embed import *

class Bet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bets = connectToBetDB().bet
        self.betters = connectToBetDB().betters

    @commands.command(name='$register')
    async def createBetter(self, ctx):
        requester_id = ctx.message.author.id
        requester_username = ctx.message.author.name
        avatar_url = ctx.message.author.avatar_url
        if self.betters.find_one({'id': requester_id}):
            await ctx.send('{name} is already registered'.format(name=ctx.message.author.name))
        else:
            user_object = {'id': requester_id,
                           'aliases': [requester_username],
                           'avatar_url': avatar_url,
                           'pushups_owed': 0,
                           'pushups_lifetime': 0,
                           'money_owed': 0,
                           'money_lifetime': 0,
                           'bets_won': 0,
                           'bets_lost': 0
                        }
            self.betters.insert_one(user_object)
            await ctx.send('{name} is now registered'.format(name=ctx.message.author.name))

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
                         'team_1': betParams[1].upper(),
                         'team_2': betParams[2].upper(),
                         'created_by_prediction': betParams[3].upper(),
                         'odds': betParams[4],
                         'amount': int(betParams[5]),
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
        await ctx.send("Listing Active Bets:")
        for doc in cur:
            await ctx.send("{team_1} vs {team_2}, Your Prediction: {prediction}, Amount: {amount}, Odds: {odds}"
                           .format(team_1=doc['team_1'], team_2=doc['team_2'], prediction=doc['created_by_prediction'],
                                   amount=doc['amount'], odds=doc['odds']))

    @commands.command(name='$winner')
    async def setWinner(self, ctx, *args):
        requester_id = ctx.message.author.id
        requester_username = ctx.message.author.name
        winnerParams = ''.join(args).split(",")
        team_1 = winnerParams[0]
        team_2 = winnerParams[1]
        winner = winnerParams[2]
        # looking for bet that does not have a winner yet
        found_bet = self.bets.find_one({
            '$and': [{"team_1": team_1},
                     {"team_2": team_2},
                     {"winner": None}
                     ]
        }) or self.bets.find_one({
            '$and': [{"team_1": team_2},
                     {"team_2": team_1},
                     {"winner": None}
                     ]
        })

        if found_bet:
            self.bets.find_one_and_update(
                {"_id": ObjectId(found_bet['_id'])},
                {"$set": {"winner": winner}}
            )

            # updating bet people stats, should prob move to separate function
            if winner == found_bet['created_by_prediction']:  # person who made bet was correct
                self.betters.find_one_and_update(
                    {"id": found_bet['created_by']},
                    {"$inc": {'bets_won': 1}}
                )
                self.betters.find_one_and_update(
                    {"aliases": {"$in": [found_bet['betting_against']]}},
                    {"$inc": {
                        'bets_lost': 1,
                        'pushups_owed': found_bet['betting_against_amount'],
                        'pushups_lifetime': found_bet['betting_against_amount']
                    }}
                )

            else:  # bet creator was incorrect
                self.betters.find_one_and_update(
                    {"id": found_bet['created_by']},
                    {"$inc": {
                        'bets_lost': 1,
                        'pushups_owed': found_bet['amount'],
                        'pushups_lifetime': found_bet['amount']
                    }}
                )
                self.betters.find_one_and_update(
                    {"aliases": {"$in": [found_bet['betting_against']]}},
                    {"$inc": {'bets_won': 1}}
                )
            await ctx.send("done")

        else:
            await ctx.send("bet was not found")

    @commands.command(name='$stats')
    async def getStats(self, ctx, user=None):
        requester_id = ctx.message.author.id
        requester_username = ctx.message.author.name

        if not user:  # self search
            doc = self.betters.find_one({'id': requester_id})
            if not doc:
                await ctx.send('user not found')
                return
        else:
            doc = self.betters.find_one(
                {"aliases": {"$in": [user]}}
            )

        await ctx.send("W-L : {wins}-{losses}, Pushups: {pushups}"
                       .format(wins=doc['bets_won'], losses=doc['bets_lost'], pushups=int(doc['pushups_owed'])))
        await ctx.send(embed=createBetterEmbed(doc))

    @commands.command(name='$test')
    async def test(self, ctx):
        pass