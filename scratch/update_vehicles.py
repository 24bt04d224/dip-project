import pymongo

def update_test_vehicles():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["smart_cctv"]
    collection = db["vehicles"]

    test_data = [
        {"plate_number": "KA02KJ9088", "owner_name": "Local Resident", "status": "Allowed"},
        {"plate_number": "GJ05TL6970", "owner_name": "SUSPECT VEHICLE", "status": "Blacklisted"},
        {"plate_number": "PB10GN4497", "owner_name": "Delivery Partner", "status": "Allowed"},
        {"plate_number": "22BH6517A", "owner_name": "Central Govt Employee", "status": "Allowed"},
        {"plate_number": "MH12DE1433", "owner_name": "Staff Member", "status": "Allowed"},
        {"plate_number": "MH15BD8877", "owner_name": "Guest Visitor", "status": "Allowed"}
    ]

    for data in test_data:
        # Upsert: Update if exists, insert if not
        collection.update_one(
            {"plate_number": data["plate_number"]},
            {"$set": data},
            upsert=True
        )
    
    print(f"Successfully registered {len(test_data)} new vehicle statuses.")

if __name__ == "__main__":
    update_test_vehicles()
