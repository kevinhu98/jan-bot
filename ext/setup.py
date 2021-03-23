import pymongo
import os
from dotenv import load_dotenv

def connectToPoeDB():
    try:
        load_dotenv()
        client = pymongo.MongoClient('mongodb+srv://kevin:{env}@cluster0.8xh0x.mongodb.net/poe.users?retryWrites=true&w=majority'.format(env=os.getenv('MONGO_PW')))
        poe_client = client.poe
    except Exception as e:
        print(e.message)

    return poe_client

def connectToBetDB():
    try:
        load_dotenv()
        client = pymongo.MongoClient('mongodb+srv://kevin:{env}@cluster0.8xh0x.mongodb.net/bets.bet?retryWrites=true&w=majority'.format(env=os.getenv('MONGO_PW')))
        bet_client = client.bets
    except Exception as e:
        print(e.message)

    return bet_client