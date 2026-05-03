import pymongo

# MongoDB setup
MONGO_URI = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["smart_cctv"]
vehicles_col = db["vehicles"]

# Data to insert
new_vehicle = {
    "plate_number": "GJ06CH2323",
    "owner_name": "Maan",
    "status": "Allowed"
}

# Update or insert
result = vehicles_col.update_one(
    {"plate_number": "GJ06CH2323"},
    {"$set": new_vehicle},
    upsert=True
)

if result.matched_count > 0:
    print(f"Updated existing record for {new_vehicle['plate_number']}")
else:
    print(f"Added new allowed vehicle: {new_vehicle['plate_number']} (Owner: {new_vehicle['owner_name']})")
