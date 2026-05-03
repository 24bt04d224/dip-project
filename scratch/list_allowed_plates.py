import pymongo

# MongoDB setup
MONGO_URI = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["smart_cctv"]
vehicles_col = db["vehicles"]

# Fetch allowed plates
allowed_vehicles = list(vehicles_col.find({"status": "Allowed"}))

print(f"Total Allowed Vehicles: {len(allowed_vehicles)}")
print("-" * 30)
for vehicle in allowed_vehicles[:20]: # Show first 20
    print(f"Plate: {vehicle['plate_number']} | Owner: {vehicle['owner_name']}")

if len(allowed_vehicles) > 20:
    print(f"... and {len(allowed_vehicles) - 20} more.")
