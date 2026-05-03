import pymongo
from bson import json_util
import json

MONGO_URI = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["smart_cctv"]
logs_col = db["logs"]

log = logs_col.find_one({"plate_number": "RJ20PA1908", "status_text": "Blacklisted"})
print(json.dumps(log, indent=2, default=json_util.default))
