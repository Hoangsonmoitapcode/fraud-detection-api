#!/usr/bin/env python3
"""
Test batch phone number analysis
"""
import requests
import json

def test_batch_phone_analysis(base_url: str = "http://localhost:8000"):
    """Test batch phone analysis endpoint"""
    
    print("📱 Testing Batch Phone Number Analysis")
    print("=" * 50)
    
    # Test data - mix of safe and unsafe numbers
    test_cases = [
        {
            "name": "Small Batch (2 numbers)",
            "phone_numbers": [
                "0965842855",  # Vietnamese (safe)
                "+12345678901"  # US (unsafe)
            ]
        },
        {
            "name": "Medium Batch (5 numbers)",
            "phone_numbers": [
                "0965842855",    # Vietnamese (safe)
                "0987654321",    # Vietnamese (safe)
                "+12345678901",  # US (unsafe)
                "+447123456789", # UK (unsafe)
                "+8613812345678" # China (unsafe)
            ]
        },
        {
            "name": "Large Batch (10 numbers)",
            "phone_numbers": [
                "0965842855", "0987654321", "0328123456",  # VN (safe)
                "+12345678901", "+447123456789", "+8613812345678",  # International (unsafe)
                "+919876543210", "+491234567890", "+79123456789",  # More international (unsafe)
                "0999888777"  # VN (safe)
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
                f"{base_url}/analyze-batch/",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                summary = data.get("summary", {})
                results = data.get("results", [])
                
                print(f"✅ SUCCESS")
                print(f"   Total analyzed: {summary.get('total_analyzed')}")
                print(f"   High risk: {summary.get('high_risk_count')}")
                print(f"   Low risk: {summary.get('low_risk_count')}")
                print(f"   Processing time: {summary.get('processing_time')}s")
                
                # Show some sample results
                print(f"   Sample results:")
                for i, result in enumerate(results[:3]):  # Show first 3
                    status = "✅" if result.get("status") == "success" else "❌"
                    print(f"     {status} {result.get('phone_number')} → {result.get('fraud_risk')}")
                
                if len(results) > 3:
                    print(f"     ... and {len(results) - 3} more")
                    
            else:
                print(f"❌ FAILED - HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ ERROR - {str(e)}")

def test_batch_edge_cases(base_url: str = "http://localhost:8000"):
    """Test edge cases for batch analysis"""
    
    print(f"\n🔹 Testing Edge Cases")
    
    edge_cases = [
        {
            "name": "Empty list",
            "phone_numbers": []
        },
        {
            "name": "Invalid phone numbers",
            "phone_numbers": ["invalid", "123", "abc"]
        },
        {
            "name": "Mixed valid/invalid",
            "phone_numbers": ["0965842855", "invalid", "+12345678901"]
        }
    ]
    
    for case in edge_cases:
        print(f"\n   Testing: {case['name']}")
        
        try:
            response = requests.post(
                f"{base_url}/analyze-batch/",
                json={"phone_numbers": case["phone_numbers"]},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                summary = data.get("summary", {})
                print(f"   ✅ Handled gracefully - {summary.get('total_analyzed')} processed")
            elif response.status_code == 422:
                print(f"   ✅ Validation error (expected for empty list)")
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

def test_performance_comparison(base_url: str = "http://localhost:8000"):
    """Compare single vs batch performance"""
    
    print(f"\n🔹 Performance Comparison")
    
    test_phones = ["0965842855", "0987654321", "0328123456", "+12345678901", "+447123456789"]
    
    import time
    
    # Test individual calls
    start_time = time.time()
    individual_results = []
    
    for phone in test_phones:
        try:
            response = requests.post(
                f"{base_url}/analyze/",
                params={"phone_number": phone}
            )
            if response.status_code == 200:
                individual_results.append(response.json())
        except:
            pass
    
    individual_time = time.time() - start_time
    
    # Test batch call
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{base_url}/analyze-batch/",
            json={"phone_numbers": test_phones},
            headers={"Content-Type": "application/json"}
        )
        batch_data = response.json() if response.status_code == 200 else None
    except:
        batch_data = None
    
    batch_time = time.time() - start_time
    
    # Results
    print(f"   Individual calls: {individual_time:.3f}s ({len(individual_results)} successful)")
    print(f"   Batch call: {batch_time:.3f}s")
    
    if batch_data and individual_results:
        improvement = (individual_time / batch_time) if batch_time > 0 else 0
        print(f"   Performance improvement: {improvement:.1f}x faster")

if __name__ == "__main__":
    print("🚀 Starting Batch Phone Analysis Tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("\n" + "=" * 60)
    
    # Run tests
    test_batch_phone_analysis()
    test_batch_edge_cases()
    test_performance_comparison()
    
    print("\n" + "=" * 60)
    print("🏁 Batch testing completed!")
