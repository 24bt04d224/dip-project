import pymongo

MONGO_URI = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["smart_cctv"]
vehicles_col = db["vehicles"]

blacklisted_vehicles = list(vehicles_col.find({"status": "Blacklisted"}))
print(f"Total Blacklisted Vehicles in Database: {len(blacklisted_vehicles)}")
for v in blacklisted_vehicles:
    print(f"- {v['plate_number']} ({v.get('owner_name', 'Unknown')})")
