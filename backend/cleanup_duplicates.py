import pymongo
from datetime import datetime

# MongoDB setup
MONGO_URI = "mongodb://localhost:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["smart_cctv"]
logs_col = db["logs"]

def cleanup():
    print("Starting cleanup of duplicate number plates...")
    
    # Get all logs
    all_logs = list(logs_col.find().sort("timestamp", 1))
    
    unique_plates = {}
    ids_to_delete = []
    
    # Simple logic: Keep only the first occurrence of a plate if it happens within 5 minutes of the previous one
    # Or just keep one entry per plate if that's what the user prefers (usually one per session).
    # Let's go with "One entry per plate per 5 minute window"
    
    for log in all_logs:
        plate = log.get("plate_number")
        timestamp_str = log.get("timestamp")
        
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except:
            continue

        if plate in unique_plates:
            last_time = unique_plates[plate]
            diff = (timestamp - last_time).total_seconds()
            
            if diff < 300: # 5 minutes cooldown
                ids_to_delete.append(log["_id"])
                continue
        
        unique_plates[plate] = timestamp

    if ids_to_delete:
        result = logs_col.delete_many({"_id": {"$in": ids_to_delete}})
        print(f"Deleted {result.deleted_count} duplicate entries.")
    else:
        print("No duplicates found.")

if __name__ == "__main__":
    cleanup()
