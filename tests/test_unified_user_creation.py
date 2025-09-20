#!/usr/bin/env python3
"""
Test unified user creation endpoint - single or multiple users
"""
import requests
import json

def test_single_user_creation(base_url: str = "http://localhost:8000"):
    """Test single user creation (backward compatibility)"""
    
    print("👤 Testing Single User Creation")
    print("=" * 50)
    
    # Single user request
    single_request = {
        "phone_numbers": ["0965111001"]  # Array with 1 item
    }
    
    try:
        response = requests.post(
            f"{base_url}/users/",
            json=single_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if it returns UserResponse format (backward compatibility)
            if "id" in data and "phone_number" in data:
                print(f"✅ SUCCESS - UserResponse format (backward compatible)")
                print(f"   User ID: {data.get('id')}")
                print(f"   Phone: {data.get('phone_number')}")
                print(f"   Region: {data.get('phone_region')}")
                print(f"   Risk: {'HIGH' if data.get('label') == 'unsafe' else 'LOW'}")
            else:
                print(f"✅ SUCCESS - Batch format")
                summary = data.get("summary", {})
                print(f"   Created: {summary.get('created_count')}")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_multiple_user_creation(base_url: str = "http://localhost:8000"):
    """Test multiple user creation"""
    
    print("\n👥 Testing Multiple User Creation")
    print("=" * 50)
    
    # Multiple users request
    batch_request = {
        "phone_numbers": [
            "0965222001",  # Vietnamese (safe)
            "0965222002",  # Vietnamese (safe)
            "+12345222001", # US (unsafe)
            "0965222003"   # Vietnamese (safe)
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/users/",
            json=batch_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Should return batch format for multiple users
            if "summary" in data:
                summary = data.get("summary", {})
                results = data.get("results", [])
                
                print(f"✅ SUCCESS - Batch format")
                print(f"   Total submitted: {summary.get('total_submitted')}")
                print(f"   Created: {summary.get('created_count')}")
                print(f"   Duplicates: {summary.get('duplicate_count')}")
                print(f"   Errors: {summary.get('error_count')}")
                print(f"   Processing time: {summary.get('processing_time')}s")
                
                # Show results
                print(f"   Results:")
                for result in results:
                    status_icon = {"created": "✅", "duplicate": "🔄", "error": "❌"}.get(result.get("status"), "❓")
                    phone = result.get("phone_number")
                    status = result.get("status")
                    risk = result.get("fraud_risk", "N/A")
                    print(f"     {status_icon} {phone} → {status} ({risk} risk)")
                    
            else:
                print(f"⚠️  Unexpected format: {data}")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_duplicate_handling(base_url: str = "http://localhost:8000"):
    """Test duplicate user handling"""
    
    print("\n🔄 Testing Duplicate Handling")
    print("=" * 50)
    
    # Create some users first
    first_batch = {
        "phone_numbers": ["0965333001", "0965333002"]
    }
    
    print("   Creating initial users...")
    try:
        response1 = requests.post(
            f"{base_url}/users/",
            json=first_batch,
            headers={"Content-Type": "application/json"}
        )
        
        if response1.status_code == 200:
            data1 = response1.json()
            if "summary" in data1:
                created1 = data1.get("summary", {}).get("created_count", 0)
                print(f"   ✅ Created {created1} users")
            else:
                print(f"   ✅ Created 1 user (single format)")
        
        # Try to create same users again (should detect duplicates)
        print("   Testing duplicate detection...")
        response2 = requests.post(
            f"{base_url}/users/",
            json=first_batch,  # Same data
            headers={"Content-Type": "application/json"}
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            if "summary" in data2:
                summary2 = data2.get("summary", {})
                created2 = summary2.get("created_count", 0)
                duplicates2 = summary2.get("duplicate_count", 0)
                
                print(f"   ✅ Second attempt: Created {created2}, Duplicates {duplicates2}")
                
                if duplicates2 > 0 and created2 == 0:
                    print(f"   ✅ Duplicate detection working correctly!")
                else:
                    print(f"   ⚠️  Unexpected duplicate handling")
                    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def test_mixed_scenarios(base_url: str = "http://localhost:8000"):
    """Test mixed scenarios (valid/invalid/duplicate)"""
    
    print("\n🎭 Testing Mixed Scenarios")
    print("=" * 50)
    
    # Mixed request with valid, invalid, and potentially duplicate numbers
    mixed_request = {
        "phone_numbers": [
            "0965444001",    # New Vietnamese (should create)
            "invalid_phone", # Invalid format (should error)
            "0965444001",    # Duplicate of first one (should detect)
            "+12345444001"   # New US number (should create)
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/users/",
            json=mixed_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "summary" in data:
                summary = data.get("summary", {})
                results = data.get("results", [])
                
                print(f"✅ SUCCESS - Mixed scenarios handled")
                print(f"   Total: {summary.get('total_submitted')}")
                print(f"   Created: {summary.get('created_count')}")
                print(f"   Duplicates: {summary.get('duplicate_count')}")
                print(f"   Errors: {summary.get('error_count')}")
                
                # Analyze results
                for i, result in enumerate(results, 1):
                    status = result.get("status")
                    phone = result.get("phone_number")
                    
                    if status == "created":
                        print(f"   ✅ {phone} - Created successfully")
                    elif status == "duplicate":
                        print(f"   🔄 {phone} - Duplicate detected")
                    elif status == "error":
                        print(f"   ❌ {phone} - Error: {result.get('message', 'Unknown error')}")
                        
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_backward_compatibility(base_url: str = "http://localhost:8000"):
    """Test that old single user format still works"""
    
    print("\n🔙 Testing Backward Compatibility")
    print("=" * 50)
    
    # Test that single user returns UserResponse format for backward compatibility
    single_request = {
        "phone_numbers": ["0965555001"]
    }
    
    try:
        response = requests.post(
            f"{base_url}/users/",
            json=single_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if it has UserResponse structure
            required_fields = ["id", "phone_number", "phone_head", "phone_region", "label"]
            has_user_fields = all(field in data for field in required_fields)
            
            if has_user_fields:
                print(f"✅ Backward compatibility maintained")
                print(f"   Returns UserResponse format for single user")
                print(f"   Fields: {list(data.keys())}")
            else:
                print(f"⚠️  Returns batch format instead of UserResponse")
                print(f"   This might break existing clients")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Unified User Creation Tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("This will CREATE USERS in your database!")
    print("\n" + "=" * 80)
    
    # Run tests
    test_single_user_creation()
    test_multiple_user_creation()
    test_duplicate_handling()
    test_mixed_scenarios()
    test_backward_compatibility()
    
    print("\n" + "=" * 80)
    print("🏁 Unified user creation testing completed!")
    print("\n🎉 Benefits of Unified Endpoint:")
    print("   ✅ Single endpoint handles 1 or multiple users")
    print("   ✅ Backward compatibility for single users")
    print("   ✅ Consistent batch format for multiple users")
    print("   ✅ Better error handling and duplicate detection")
    print("   ✅ Cleaner API design")
    print("   ✅ Reduced maintenance overhead")

