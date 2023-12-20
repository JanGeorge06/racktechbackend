from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "SECRET!!!"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#DB Collections
db = client['racktech']
users_collection = db['users']
products_collection = db['products']
