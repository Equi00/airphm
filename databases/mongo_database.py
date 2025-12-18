from pymongo import MongoClient

client = MongoClient("localhost", 27017)

db = client.Airphm_db

collection_name = db["accommodation"]