
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print(f"Testing Health Check: {BASE_URL}/health")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health Check Passed!")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return False

def test_query():
    print(f"\nTesting Query Endpoint: {BASE_URL}/query")
    payload = {"query": "What is ROS 2?"}
    try:
        response = requests.post(f"{BASE_URL}/query", json=payload)
        if response.status_code == 200:
            print("✅ Query Check Passed!")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print(f"❌ Query Check Failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return False

if __name__ == "__main__":
    health = test_health()
    if health:
        test_query()
