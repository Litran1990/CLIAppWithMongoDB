import pymongo
import os

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "myTestDB"
COLLECTION_NAME = "myFirstMDB"

""" Connection String """
def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e
        
conn = mongo_connect(MONGODB_URI)
        
coll = conn[DBS_NAME][COLLECTION_NAME]

# Very similar to how we did from the command line, we'll do coll.find.
documents = coll.find()

for doc in documents:
    print(doc)