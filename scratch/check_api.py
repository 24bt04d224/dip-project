import requests
try:
    r = requests.get("http://localhost:5000/stats", timeout=5)
    print(r.json())
except Exception as e:
    print(f"Error: {e}")
