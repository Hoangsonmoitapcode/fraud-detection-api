#!/usr/bin/env python3
"""
Test batch user creation - saves to database
"""
import requests
import json

def test_batch_user_creation(base_url: str = "http://localhost:8000"):
    """Test batch user creation endpoint that saves to database"""
    
    print("👥 Testing Batch User Creation (Database Save)")
    print("=" * 50)
    
    # Test data - mix of new and potentially duplicate numbers
    test_cases = [
        {
            "name": "Small Batch (3 numbers)",
            "phone_numbers": [
                "0965000001",  # New Vietnamese number
                "0965000002",  # New Vietnamese number
                "+12340000001"  # New US number
            ]
        },
        {
            "name": "Mixed Valid/Invalid",
            "phone_numbers": [
                "0965000003",    # New Vietnamese (valid)
                "invalid_phone", # Invalid format
                "+12340000002"   # New US (valid)
            ]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🔹 Testing: {test_case['name']}")
        
        try:
            # Prepare request
            request_data = {
                "phone_numbers": test_case["phone_numbers"]
            }
            
            # Send request
            response = requests.post(
                f"{base_url}/users-batch/",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                summary = data.get("summary", {})
                results = data.get("results", [])
                
                print(f"✅ SUCCESS")
                print(f"   Total submitted: {summary.get('total_submitted')}")
                print(f"   Created: {summary.get('created_count')}")
                print(f"   Duplicates: {summary.get('duplicate_count')}")
                print(f"   Errors: {summary.get('error_count')}")
                print(f"   Processing time: {summary.get('processing_time')}s")
                
                # Show detailed results
                print(f"   Detailed results:")
                for result in results:
                    status_icon = {
                        "created": "✅",
                        "duplicate": "🔄", 
                        "error": "❌"
                    }.get(result.get("status"), "❓")
                    
                    phone = result.get("phone_number")
                    status = result.get("status")
                    user_id = result.get("user_id", "N/A")
                    
                    print(f"     {status_icon} {phone} → {status} (ID: {user_id})")
                    
            else:
                print(f"❌ FAILED - HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ ERROR - {str(e)}")

def test_duplicate_handling(base_url: str = "http://localhost:8000"):
    """Test duplicate handling - same numbers twice"""
    
    print(f"\n🔹 Testing Duplicate Handling")
    
    # First batch - create users
    first_batch = {
        "phone_numbers": ["0965999001", "0965999002"]
    }
    
    print(f"   First batch (should create)...")
    try:
        response1 = requests.post(
            f"{base_url}/users-batch/",
            json=first_batch,
            headers={"Content-Type": "application/json"}
        )
        
        if response1.status_code == 200:
            data1 = response1.json()
            created_count1 = data1.get("summary", {}).get("created_count", 0)
            print(f"   ✅ Created {created_count1} users")
        else:
            print(f"   ❌ Failed: {response1.status_code}")
            return
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return
    
    # Second batch - same numbers (should detect duplicates)
    print(f"   Second batch (should detect duplicates)...")
    try:
        response2 = requests.post(
            f"{base_url}/users-batch/",
            json=first_batch,  # Same data
            headers={"Content-Type": "application/json"}
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            summary2 = data2.get("summary", {})
            created_count2 = summary2.get("created_count", 0)
            duplicate_count2 = summary2.get("duplicate_count", 0)
            
            print(f"   ✅ Created: {created_count2}, Duplicates: {duplicate_count2}")
            
            if duplicate_count2 == 2 and created_count2 == 0:
                print(f"   ✅ Duplicate detection working correctly!")
            else:
                print(f"   ⚠️  Unexpected results")
                
        else:
            print(f"   ❌ Failed: {response2.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def verify_database_updates(base_url: str = "http://localhost:8000"):
    """Verify that users were actually created in database"""
    
    print(f"\n🔹 Verifying Database Updates")
    
    # Create some test users
    test_numbers = ["0965888001", "0965888002", "+12348880001"]
    
    print(f"   Creating test users...")
    try:
        response = requests.post(
            f"{base_url}/users-batch/",
            json={"phone_numbers": test_numbers},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            created_count = data.get("summary", {}).get("created_count", 0)
            print(f"   ✅ Created {created_count} users")
            
            # Show user IDs that were created
            results = data.get("results", [])
            created_users = [r for r in results if r.get("status") == "created"]
            
            if created_users:
                print(f"   Created user IDs:")
                for user in created_users:
                    phone = user.get("phone_number")
                    user_id = user.get("user_id")
                    analysis = user.get("analysis", {})
                    region = analysis.get("phone_region", "Unknown")
                    risk = user.get("fraud_risk", "Unknown")
                    
                    print(f"     ID {user_id}: {phone} ({region}) - {risk} risk")
            
        else:
            print(f"   ❌ Failed to create users: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Batch User Creation Tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("This will CREATE USERS in your database!")
    print("\n" + "=" * 60)
    
    # Run tests
    test_batch_user_creation()
    test_duplicate_handling()
    verify_database_updates()
    
    print("\n" + "=" * 60)
    print("🏁 Batch user creation testing completed!")
    print("💾 Check your database - new users should be created!")
