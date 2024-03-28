from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://setoftest:zleWRqUfrWAV1GBP@cluster0.tquohbk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

db = client.goit_ds_02
# Send a ping to confirm a successful connection
try:
    result_one = db.cats.insert_one(
        {
            "name": "Murchyk",
            "age": 3,
            "features": ["грайливий", "дає себе гладити", "рудий"],
        }
    )
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
