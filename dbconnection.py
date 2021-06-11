from pymongo import MongoClient

MONGO_URI = "mongodb+srv://abhinav:abhinav123@csd3444.cl9ms.mongodb.net/sample_analytics?retryWrites=true&w=majority"

mongodb_client = MongoClient(MONGO_URI)
db = mongodb_client.sample_analytics
