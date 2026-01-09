#!/usr/bin/env python3
"""
Debug script to test cart functionality directly
Run this to verify if the cart logic is working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.order import Cart
from models.product import Product
from models.database import execute_query

def test_cart_functionality():
    """Test cart operations directly"""
    print("🧪 Testing Cart Functionality")
    print("=" * 50)
    
    # Test user ID (you can change this to match your test user)
    test_user_id = 1
    test_product_id = 1
    
    print(f"Testing with User ID: {test_user_id}, Product ID: {test_product_id}")
    
    # Step 1: Clear cart for clean test
    print("\n1. Clearing cart for clean test...")
    Cart.clear_cart(test_user_id)
    initial_count = Cart.get_cart_count(test_user_id)
    print(f"   Initial cart count: {initial_count}")
    
    # Step 2: Add product with quantity 1
    print("\n2. Adding product with quantity 1...")
    result1 = Cart.add_to_cart(test_user_id, test_product_id, 1)
    count1 = Cart.get_cart_count(test_user_id)
    print(f"   Add result: {result1}")
    print(f"   Cart count after adding 1: {count1}")
    
    # Step 3: Add same product with quantity 2 (should become 3 total)
    print("\n3. Adding same product with quantity 2...")
    result2 = Cart.add_to_cart(test_user_id, test_product_id, 2)
    count2 = Cart.get_cart_count(test_user_id)
    print(f"   Add result: {result2}")
    print(f"   Cart count after adding 2 more: {count2}")
    print(f"   Expected: 3, Actual: {count2}")
    
    # Step 4: Add same product with quantity 3 (should become 6 total)
    print("\n4. Adding same product with quantity 3...")
    result3 = Cart.add_to_cart(test_user_id, test_product_id, 3)
    count3 = Cart.get_cart_count(test_user_id)
    print(f"   Add result: {result3}")
    print(f"   Cart count after adding 3 more: {count3}")
    print(f"   Expected: 6, Actual: {count3}")
    
    # Step 5: Check cart items details
    print("\n5. Checking cart items details...")
    cart_items = Cart.get_cart_items(test_user_id)
    print(f"   Number of different products in cart: {len(cart_items)}")
    
    for item in cart_items:
        print(f"   Product: {item.get('name', 'Unknown')} (ID: {item.get('product_id')})")
        print(f"   Quantity: {item.get('quantity')}")
        print(f"   Price: ${item.get('price', 0):.2f}")
        print(f"   Subtotal: ${item.get('subtotal', 0):.2f}")
        print()
    
    # Step 6: Test with different product
    print("6. Testing with different product...")
    test_product_id_2 = 2
    result4 = Cart.add_to_cart(test_user_id, test_product_id_2, 2)
    count4 = Cart.get_cart_count(test_user_id)
    print(f"   Added product {test_product_id_2} with quantity 2")
    print(f"   Total cart count: {count4}")
    print(f"   Expected: 8 (6 + 2), Actual: {count4}")
    
    # Step 7: Final cart state
    print("\n7. Final cart state...")
    final_items = Cart.get_cart_items(test_user_id)
    total_items = sum(item.get('quantity', 0) for item in final_items)
    print(f"   Products in cart: {len(final_items)}")
    print(f"   Total items (manual count): {total_items}")
    print(f"   Total items (get_cart_count): {Cart.get_cart_count(test_user_id)}")
    
    # Step 8: Test database directly
    print("\n8. Testing database query directly...")
    direct_query = "SELECT product_id, quantity FROM cart WHERE user_id = %s"
    direct_result = execute_query(direct_query, (test_user_id,), fetch=True)
    
    if direct_result:
        print("   Direct database results:")
        total_direct = 0
        for row in direct_result:
            product_id = row['product_id']
            quantity = row['quantity']
            total_direct += quantity
            print(f"   Product {product_id}: {quantity} items")
        print(f"   Total from direct query: {total_direct}")
    else:
        print("   No items found in database")
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print(f"   Expected final count: 8")
    print(f"   Actual final count: {Cart.get_cart_count(test_user_id)}")
    
    if Cart.get_cart_count(test_user_id) == 8:
        print("   ✅ Cart functionality is working correctly!")
    else:
        print("   ❌ Cart functionality has issues!")
    
    return Cart.get_cart_count(test_user_id) == 8

def test_product_exists():
    """Check if test products exist"""
    print("\n🔍 Checking if test products exist...")
    
    product1 = Product.get_by_id(1)
    product2 = Product.get_by_id(2)
    
    if product1:
        print(f"   ✅ Product 1: {product1.name} (Stock: {product1.stock_quantity})")
    else:
        print("   ❌ Product 1 not found")
    
    if product2:
        print(f"   ✅ Product 2: {product2.name} (Stock: {product2.stock_quantity})")
    else:
        print("   ❌ Product 2 not found")
    
    return product1 is not None and product2 is not None

if __name__ == "__main__":
    print("🚀 Cart Debug Script")
    print("Make sure your database is running and populated with sample data")
    print()
    
    try:
        # Check if products exist
        if not test_product_exists():
            print("❌ Test products not found. Make sure sample data is loaded.")
            sys.exit(1)
        
        # Test cart functionality
        success = test_cart_functionality()
        
        if success:
            print("\n🎉 All tests passed! Cart functionality is working correctly.")
        else:
            print("\n💥 Tests failed! There's an issue with cart functionality.")
            
    except Exception as e:
        print(f"\n💥 Error during testing: {e}")
        import traceback
        traceback.print_exc()