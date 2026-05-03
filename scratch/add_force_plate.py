import pymongo

# MongoDB setup
MONGO_URI = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["smart_cctv"]
vehicles_col = db["vehicles"]

# Data to insert
new_vehicle = {
    "plate_number": "GJ06LM2323",
    "owner_name": "Force Written Plate",
    "status": "Allowed"
}

# Update or insert
result = vehicles_col.update_one(
    {"plate_number": "GJ06LM2323"},
    {"$set": new_vehicle},
    upsert=True
)

print(f"Added/Updated allowed vehicle: {new_vehicle['plate_number']}")
