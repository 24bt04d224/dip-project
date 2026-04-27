import pymongo
import random
import string

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "smart_cctv"
COLLECTION_NAME = "vehicles"

def generate_indian_plate():
    # Format: XX 00 XX 0000 (e.g., MH 12 AB 1234)
    states = ["MH", "DL", "KA", "TN", "GJ", "HR", "UP", "WB", "PB", "RJ"]
    state = random.choice(states)
    district_code = f"{random.randint(1, 99):02d}"
    series = "".join(random.choices(string.ascii_uppercase, k=2))
    number = f"{random.randint(1, 9999):04d}"
    return f"{state}{district_code}{series}{number}"

def seed_database():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Clear existing data
    collection.delete_many({})

    first_names = ["Rahul", "Anjali", "Vikram", "Sneha", "Amit", "Priya", "Suresh", "Meera", "Arjun", "Kavita"]
    last_names = ["Sharma", "Verma", "Gupta", "Singh", "Patel", "Reddy", "Iyer", "Khan", "Joshi", "Das"]
    vehicle_types = ["Car", "SUV", "Sedan", "Hatchback", "Luxury"]
    statuses = ["Allowed", "Allowed", "Allowed", "Allowed", "Blacklisted", "VIP"]

    vehicles = []
    plates_seen = set()

    print("Generating 1000 vehicle records...")
    
    # Add some dedicated test plates first
    test_plates = [
        {"plate": "MH12AB1234", "owner": "John Doe (VIP)", "type": "Luxury Sedan", "status": "VIP"},
        {"plate": "DL1CAA1234", "owner": "Jane Smith", "type": "SUV", "status": "Allowed"},
        {"plate": "RJ12CV0002", "owner": "User Tester", "type": "Test Car", "status": "Allowed"},
        {"plate": "GJ05L6970", "owner": "Rahul Kumar", "type": "Hatchback", "status": "Blacklisted"}
    ]

    for tp in test_plates:
        vehicles.append({
            "plate_number": tp["plate"],
            "owner_name": tp["owner"],
            "vehicle_type": tp["type"],
            "status": tp["status"]
        })
        plates_seen.add(tp["plate"])

    for _ in range(1000 - len(test_plates)):
        plate = generate_indian_plate()
        while plate in plates_seen:
            plate = generate_indian_plate()
        plates_seen.add(plate)

        owner = f"{random.choice(first_names)} {random.choice(last_names)}"
        v_type = random.choice(vehicle_types)
        status = random.choice(statuses)

        vehicles.append({
            "plate_number": plate,
            "owner_name": owner,
            "vehicle_type": v_type,
            "status": status
        })

    collection.insert_many(vehicles)
    print(f"Successfully seeded {len(vehicles)} records into MongoDB.")

if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print("Please ensure MongoDB is running on localhost:27017")
