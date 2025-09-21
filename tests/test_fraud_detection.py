#!/usr/bin/env python3
"""
Test cases for fraud detection system - 10 different regions
"""
import requests
import json
from typing import List, Dict

# Test cases for 10 different regions
TEST_CASES = [
    # Vietnam (SAFE)
    {
        "phone_number": "0965842855",
        "expected_region": "Vietnam",
        "expected_status": "safe",
        "expected_risk": "LOW",
        "description": "Vietnamese mobile number"
    },
    
    # USA (UNSAFE)
    {
        "phone_number": "+12345678901",
        "expected_region": "USA/Canada",
        "expected_status": "unsafe", 
        "expected_risk": "HIGH",
        "description": "US phone number"
    },
    
    # United Kingdom (UNSAFE)
    {
        "phone_number": "+447123456789",
        "expected_region": "United Kingdom",
        "expected_status": "unsafe",
        "expected_risk": "HIGH", 
        "description": "UK phone number"
    },
    
    # China (UNSAFE)
    {
        "phone_number": "+8613812345678",
        "expected_region": "China",
        "expected_status": "unsafe",
        "expected_risk": "HIGH",
        "description": "Chinese phone number"
    },
    
    # India (UNSAFE)
    {
        "phone_number": "+919876543210",
        "expected_region": "India", 
        "expected_status": "unsafe",
        "expected_risk": "HIGH",
        "description": "Indian phone number"
    },
    
    # Germany (UNSAFE)
    {
        "phone_number": "+491234567890",
        "expected_region": "Germany",
        "expected_status": "unsafe",
        "expected_risk": "HIGH",
        "description": "German phone number"
    },
    
    # Russia (UNSAFE)
    {
        "phone_number": "+79123456789",
        "expected_region": "Russia",
        "expected_status": "unsafe",
        "expected_risk": "HIGH",
        "description": "Russian phone number"
    },
    
    # Nigeria (UNSAFE)
    {
        "phone_number": "+2348012345678",
        "expected_region": "Nigeria",
        "expected_status": "unsafe",
        "expected_risk": "HIGH",
        "description": "Nigerian phone number (common fraud origin)"
    },
    
    # Thailand (UNSAFE)
    {
        "phone_number": "+66812345678",
        "expected_region": "Thailand",
        "expected_status": "unsafe",
        "expected_risk": "HIGH",
        "description": "Thai phone number"
    },
    
    # Unknown Region (UNSAFE)
    {
        "phone_number": "+999123456789",
        "expected_region": "Unknown",
        "expected_status": "unsafe",
        "expected_risk": "HIGH",
        "description": "Unknown country code (potential fraud)"
    }
]

def test_phone_analysis(base_url: str = "http://localhost:8000") -> None:
    """Test phone number analysis for all regions"""
    
    print("🔍 Testing Fraud Detection System - 10 Regions")
    print("=" * 60)
    
    passed_tests = 0
    failed_tests = 0
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n📱 Test {i}: {test_case['description']}")
        print(f"   Phone: {test_case['phone_number']}")
        
        try:
            # Test analysis endpoint
            response = requests.post(
                f"{base_url}/analyze/",
                params={"phone_number": test_case['phone_number']}
            )
            
            if response.status_code == 200:
                data = response.json()
                analysis = data.get("analysis", {})
                fraud_risk = data.get("fraud_risk", "")
                
                # Check results
                region_match = analysis.get("phone_region") == test_case["expected_region"]
                status_match = analysis.get("label") == test_case["expected_status"] 
                risk_match = fraud_risk == test_case["expected_risk"]
                
                if region_match and status_match and risk_match:
                    print(f"   ✅ PASSED")
                    print(f"      Region: {analysis.get('phone_region')}")
                    print(f"      Status: {analysis.get('label')}")
                    print(f"      Risk: {fraud_risk}")
                    print(f"      Head: {analysis.get('phone_head')}")
                    passed_tests += 1
                else:
                    print(f"   ❌ FAILED")
                    print(f"      Expected: {test_case['expected_region']}, {test_case['expected_status']}, {test_case['expected_risk']}")
                    print(f"      Got: {analysis.get('phone_region')}, {analysis.get('label')}, {fraud_risk}")
                    failed_tests += 1
            else:
                print(f"   ❌ FAILED - HTTP {response.status_code}")
                failed_tests += 1
                
        except Exception as e:
            print(f"   ❌ ERROR - {str(e)}")
            failed_tests += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 TEST SUMMARY")
    print(f"   ✅ Passed: {passed_tests}")
    print(f"   ❌ Failed: {failed_tests}")
    print(f"   📈 Success Rate: {(passed_tests/(passed_tests+failed_tests)*100):.1f}%")
    
    if failed_tests == 0:
        print("\n🎉 All tests passed! Fraud detection system is working correctly!")
    else:
        print(f"\n⚠️  {failed_tests} tests failed. Please check the system.")

def test_user_creation(base_url: str = "http://localhost:8000") -> None:
    """Test user creation with auto-detection"""
    
    print("\n" + "=" * 60)
    print("👤 Testing PhoneNumber Creation with Auto-Detection")
    print("=" * 60)
    
    # Test with Vietnamese number (should be safe)
    test_phone = "0328123456"
    
    try:
        response = requests.post(
            f"{base_url}/users/",
            json={"phone_number": test_phone},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ PhoneNumber created successfully:")
            print(f"   ID: {user_data.get('id')}")
            print(f"   Phone: {user_data.get('phone_number')}")
            print(f"   Head: {user_data.get('phone_head')}")
            print(f"   Region: {user_data.get('phone_region')}")
            print(f"   Status: {user_data.get('label')}")
            print(f"   Heading ID: {user_data.get('heading_id')}")
        else:
            print(f"❌ PhoneNumber creation failed - HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error creating user: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Fraud Detection Tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    
    # Test phone analysis
    test_phone_analysis()
    
    # Test user creation
    test_user_creation()
    
    print("\n🏁 Testing completed!")
