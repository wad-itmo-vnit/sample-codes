from pymongo import MongoClient

mongo = MongoClient('localhost', 27017)

db = mongo['wad-vnit']

for user in db.users.find({}):
    print(user)