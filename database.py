import pymongo 
mongoClient = pymongo.MongoClient("mongodb+srv://admin:RaspberryPi19!@cluster0.ne4mv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
ActionTags = mongoClient['ActionTags']
Pornstars = mongoClient['PornStars']
def save_to_db(actionTag):
    ActionTags[actionTag['dataTagName']].insert_one(actionTag)
def save_pornstars(pornstar):
    Pornstars['PornStars'].insert_one(pornstar)


