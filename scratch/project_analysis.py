import pymongo
from datetime import datetime

MONGO_URI = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["smart_cctv"]
logs_col = db["logs"]
vehicles_col = db["vehicles"]

total_logs = logs_col.count_documents({"status": "success"})
unique_plates = len(logs_col.distinct("plate_number", {"status": "success"}))
unknown_vehicles = logs_col.count_documents({"status": "success", "found": False})
registered_vehicles = vehicles_col.count_documents({})

# Type breakdown
types = logs_col.aggregate([
    {"$match": {"status": "success"}},
    {"$group": {"_id": "$type", "count": {"$sum": 1}}}
])

print(f"--- Project Detection Analysis ---")
print(f"Total Detections Logged: {total_logs}")
print(f"Unique Vehicles Identified: {unique_plates}")
print(f"Unknown (Unregistered) Detections: {unknown_vehicles}")
print(f"Total Registered Vehicles in DB: {registered_vehicles}")
print("\n--- Detection Breakdown by Type ---")
for t in types:
    print(f"{t['_id']}: {t['count']}")

# Recent activity
recent = list(logs_col.find({"status": "success"}).sort("timestamp", -1).limit(5))
print("\n--- Last 5 Detections ---")
for log in recent:
    print(f"[{log['timestamp']}] {log['plate_number']} ({log['type']}) - Owner: {log.get('owner_name', 'Unknown')}")
