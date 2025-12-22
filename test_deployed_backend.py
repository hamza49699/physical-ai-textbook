"""
Test script for deployed Hugging Face backend
"""
import requests
import json

BASE_URL = "https://hamzakhan123-physical-ai-textbook.hf.space"

def test_root():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_health_db():
    """Test database health endpoint"""
    print("\n=== Testing Database Health ===")
    try:
        response = requests.get(f"{BASE_URL}/health/db")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_health_qdrant():
    """Test Qdrant health endpoint"""
    print("\n=== Testing Qdrant Health ===")
    try:
        response = requests.get(f"{BASE_URL}/health/qdrant")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_query():
    """Test query endpoint"""
    print("\n=== Testing Query Endpoint ===")
    try:
        payload = {
            "query": "What is ROS2?",
            "use_rag": True
        }
        response = requests.post(
            f"{BASE_URL}/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_documents():
    """Test documents listing endpoint"""
    print("\n=== Testing Documents Endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/documents")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Physical AI Textbook Backend")
    print(f"URL: {BASE_URL}")
    print("=" * 60)
    
    results = {
        "Root": test_root(),
        "Health": test_health(),
        "Health/DB": test_health_db(),
        "Health/Qdrant": test_health_qdrant(),
        "Query": test_query(),
        "Documents": test_documents()
    }
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for endpoint, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{endpoint:20} {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
