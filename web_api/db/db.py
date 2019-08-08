from pymongo import MongoClient
from config import MONGOSERVER, DBNAME


client = MongoClient(**MONGOSERVER)
db = client[DBNAME]