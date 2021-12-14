import pymongo 
mongoClient = pymongo.MongoClient("mongodb+srv://admin:RaspberryPi19!@cluster0.ne4mv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
ActionTags = mongoClient['ActionTags']

def save_to_db(actionTag):
    ActionTags[actionTag['dataTagName']].insert_one(actionTag)

