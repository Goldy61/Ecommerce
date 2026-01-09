#!/usr/bin/env python3
"""
Test script to verify cart button functionality
Run this after starting the Flask server to test cart operations
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://127.0.0.1:5000"
TEST_USER = {
    "username": "testuser",
    "password": "testpass123",
    "email": "test@example.com"
}

def test_cart_operations():
    """Test cart add, update, and remove operations"""
    session = requests.Session()
    
    print("🧪 Testing Cart Button Functionality")
    print("=" * 50)
    
    # Step 1: Register/Login user
    print("1. Logging in user...")
    login_data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    }
    
    response = session.post(f"{BASE_URL}/login", data=login_data)
    if response.status_code != 200:
        print("❌ Login failed. Make sure test user exists or create one.")
        return False
    
    print("✅ User logged in successfully")
    
    # Step 2: Test adding to cart
    print("\n2. Testing add to cart...")
    add_data = {
        "product_id": 1,
        "quantity": 1
    }
    
    response = session.post(
        f"{BASE_URL}/api/cart/add",
        json=add_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print(f"✅ Add to cart: {result.get('message')}")
            print(f"   Cart count: {result.get('cart_count')}")
        else:
            print(f"❌ Add to cart failed: {result.get('message')}")
            return False
    else:
        print(f"❌ Add to cart request failed: {response.status_code}")
        return False
    
    # Step 3: Test rapid update operations (simulate double-clicking)
    print("\n3. Testing rapid quantity updates (simulating double-clicks)...")
    
    # Simulate rapid clicks on increase button
    for i in range(3):
        update_data = {
            "product_id": 1,
            "quantity": 2 + i
        }
        
        response = session.post(
            f"{BASE_URL}/api/cart/update",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"   Update {i+1}: quantity={2+i}, cart_count={result.get('cart_count')}")
            else:
                print(f"   Update {i+1} failed: {result.get('message')}")
        
        # Small delay to simulate rapid clicking
        time.sleep(0.1)
    
    # Step 4: Get final cart state
    print("\n4. Checking final cart state...")
    response = session.get(f"{BASE_URL}/api/cart/count")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Final cart count: {result.get('cart_count')}")
    
    # Step 5: Test remove from cart
    print("\n5. Testing remove from cart...")
    remove_data = {
        "product_id": 1
    }
    
    response = session.post(
        f"{BASE_URL}/api/cart/remove",
        json=remove_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print(f"✅ Remove from cart: {result.get('message')}")
            print(f"   Final cart count: {result.get('cart_count')}")
        else:
            print(f"❌ Remove from cart failed: {result.get('message')}")
    
    print("\n🎉 Cart functionality test completed!")
    return True

if __name__ == "__main__":
    print("Make sure the Flask server is running on http://127.0.0.1:5000")
    print("Press Enter to start testing...")
    input()
    
    try:
        test_cart_operations()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server. Make sure it's running on port 5000.")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")