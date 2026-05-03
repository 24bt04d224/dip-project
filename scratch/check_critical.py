import pymongo

MONGO_URI = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["smart_cctv"]
logs_col = db["logs"]

critical_count = logs_col.count_documents({"status": "success", "status_text": "Blacklisted"})
print(f"Critical Alerts Count: {critical_count}")

# Also list unique critical plates
unique_plates = logs_col.distinct("plate_number", {"status": "success", "status_text": "Blacklisted"})
print(f"Unique Critical Plates: {len(unique_plates)}")
for plate in unique_plates:
    print(f"- {plate}")
