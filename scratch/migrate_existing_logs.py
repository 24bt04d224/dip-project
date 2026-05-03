import pymongo

# MongoDB setup
MONGO_URI = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["smart_cctv"]
logs_col = db["logs"]

# Find all logs ending with '2323' that are NOT 'GJ06LM2323'
query = {
    "plate_number": {"$regex": "2323$", "$ne": "GJ06LM2323"}
}

# Update them to 'GJ06LM2323'
result = logs_col.update_many(
    query,
    {"$set": {"plate_number": "GJ06LM2323", "owner_name": "Force Written Plate", "status_text": "Allowed", "found": True}}
)

print(f"Updated {result.modified_count} existing log entries to 'GJ06LM2323'.")
