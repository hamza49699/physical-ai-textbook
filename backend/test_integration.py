
from fastapi import FastAPI
from httpx import Client, ASGITransport
from main import app
import os
import sys

# Add current directory to path so we can import main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Use ASGITransport for testing FastAPI app directly without TestClient wrapper issues
transport = ASGITransport(app=app)
client = Client(transport=transport, base_url="http://test")

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    print("Response JSON:", response.json())
    assert "Physical AI Textbook API" in response.json()["message"]

def test_health_check():
    print("\nTesting /health endpoint...")
    response = client.get("/health")
    
    print(f"Health Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code in [200, 503]

if __name__ == "__main__":
    try:
        print("Starting tests...")
        test_root()
        print("Root endpoint passed")
        test_health_check()
        print("Health check execution passed")
    except Exception as e:
        print(f"Tests failed: {e}")
