import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["smart_cctv"]
vehicles_col = db["vehicles"]

plate = "HR98AA0000"

# Insert or Update the specific vehicle
result = vehicles_col.update_one(
    {"plate_number": plate},
    {"$set": {
        "owner_name": "Alert: Unauthorized Vehicle",
        "status": "Blacklisted",
        "last_seen": "Never"
    }},
    upsert=True
)

print(f"Vehicle {plate} has been added to the BLACKLIST.")
if result.upserted_id:
    print(f"New record created.")
else:
    print(f"Existing record updated.")
