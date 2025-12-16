import requests
import json

print("Testing backend endpoints...")
print("=" * 50)

# Test 1: Root endpoint
try:
    response = requests.get("http://localhost:8000/")
    print(f"✓ Root endpoint: {response.status_code}")
    print(f"  Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"✗ Root endpoint failed: {e}")

print("\n" + "=" * 50)

# Test 2: Health endpoint
try:
    response = requests.get("http://localhost:8000/health")
    print(f"✓ Health endpoint: {response.status_code}")
    print(f"  Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"✗ Health endpoint failed: {e}")

print("\n" + "=" * 50)

# Test 3: Query endpoint
try:
    response = requests.post(
        "http://localhost:8000/query",
        json={"query": "What is physical AI?"}
    )
    print(f"✓ Query endpoint: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"  Query: {result.get('query', 'N/A')}")
        print(f"  Response preview: {result.get('response', 'N/A')[:100]}...")
        print(f"  Sources: {result.get('sources', [])}")
        print(f"  Confidence: {result.get('confidence', 0)}")
    else:
        print(f"  Error: {response.text}")
except Exception as e:
    print(f"✗ Query endpoint failed: {e}")

print("\n" + "=" * 50)
print("Backend testing complete!")
