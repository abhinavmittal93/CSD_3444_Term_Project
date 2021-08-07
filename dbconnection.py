from pymongo import MongoClient
import ssl

# MongoDB URI
MONGO_URI = "mongodb+srv://abhinav:abhinav123@csd3444.cl9ms.mongodb.net/college_admission_management?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

# Creating single instance for the mongodb client
mongodb_client = MongoClient(MONGO_URI)
db = mongodb_client.college_admission_management
