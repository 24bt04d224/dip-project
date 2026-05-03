import pymongo
from bson.json_util import dumps

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["smart_cctv"]
logs_col = db["logs"]

print("--- Last 5 Detected Vehicles (Logs) ---")
recent_logs = logs_col.find().sort("timestamp", -1).limit(5)
for log in recent_logs:
    print(f"Plate: {log.get('plate_number')} | Time: {log.get('timestamp')} | Status: {log.get('status_text')} | Confidence: {log.get('confidence')}%")

print("\n--- Summary ---")
print(f"Total Detections Logged: {logs_col.count_documents({})}")
