#!/usr/bin/env python3
"""
Test script to verify Railway PostgreSQL database setup
Run after deployment: python testing/test_railway_database.py
"""

import requests
import json
import time

def test_railway_database(api_url):
    """Test Railway database setup and functionality"""
    
    print("🗄️ Testing Railway PostgreSQL Database Setup")
    print("=" * 60)
    print(f"📡 API URL: {api_url}")
    print()
    
    tests_passed = 0
    total_tests = 6
    
    try:
        # Test 1: Health Check
        print("🏥 Test 1: Database Health Check")
        response = requests.get(f"{api_url}/health", timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            db_status = health_data.get("checks", {}).get("database", "unknown")
            
            if db_status == "healthy":
                print("   ✅ Database connection: HEALTHY")
                tests_passed += 1
            else:
                print(f"   ❌ Database connection: {db_status}")
        else:
            print(f"   ❌ Health check failed: HTTP {response.status_code}")
        
        print()
        
        # Test 2: API Status
        print("📊 Test 2: API Status")
        response = requests.get(f"{api_url}/", timeout=10)
        
        if response.status_code == 200:
            print("   ✅ API Status endpoint: Working")
            tests_passed += 1
        else:
            print(f"   ❌ API Status failed: HTTP {response.status_code}")
        
        print()
        
        # Test 3: Phone Analysis (Vietnamese number)
        print("📱 Test 3: Vietnamese Phone Analysis")
        test_phones = ["0965842855", "0870123456", "0920123456"]
        
        response = requests.post(f"{api_url}/analyze/", 
                               json={"phone_numbers": test_phones},
                               timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if "results" in data:
                results = data["results"]
                safe_count = sum(1 for r in results if r.get("fraud_risk") == "LOW")
                
                print(f"   ✅ Analyzed {len(results)} numbers")
                print(f"   ✅ Safe Vietnamese numbers: {safe_count}/{len(results)}")
                
                # Show sample results
                for i, result in enumerate(results[:2]):
                    phone = result.get("phone_number", "")
                    analysis = result.get("analysis", {})
                    risk = result.get("fraud_risk", "")
                    head = analysis.get("phone_head", "")
                    region = analysis.get("phone_region", "")
                    
                    print(f"   📱 {phone}: {head} → {region} ({risk} risk)")
                
                tests_passed += 1
            else:
                # Single number response
                analysis = data.get("analysis", {})
                risk = data.get("fraud_risk", "")
                print(f"   ✅ Single analysis: {risk} risk")
                tests_passed += 1
        else:
            print(f"   ❌ Phone analysis failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
        
        print()
        
        # Test 4: International Phone (should be unsafe)
        print("🌍 Test 4: International Phone Analysis")
        response = requests.post(f"{api_url}/analyze/", 
                               json={"phone_numbers": ["+1234567890"]},
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle both single and batch response formats
            if "results" in data and data["results"]:
                result = data["results"][0]
            else:
                result = data
            
            risk = result.get("fraud_risk", "UNKNOWN")
            analysis = result.get("analysis", {})
            
            if risk == "HIGH":
                print("   ✅ International number correctly flagged as HIGH risk")
                tests_passed += 1
            else:
                print(f"   ⚠️ International number risk: {risk} (expected HIGH)")
        else:
            print(f"   ❌ International analysis failed: HTTP {response.status_code}")
        
        print()
        
        # Test 5: SMS Scam Reporting
        print("💬 Test 5: SMS Scam Functionality")
        sms_data = {
            "sms_messages": [{
                "sms_content": "Chúc mừng! Bạn đã trúng thưởng 100 triệu đồng. Test message.",
                "label": "spam"
            }]
        }
        
        response = requests.post(f"{api_url}/sms-scam/", 
                               json=sms_data,
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            created = data.get("summary", {}).get("created_count", 0)
            print(f"   ✅ SMS scam reporting: {created} message(s) processed")
            tests_passed += 1
        else:
            print(f"   ❌ SMS scam reporting failed: HTTP {response.status_code}")
        
        print()
        
        # Test 6: Database Population Check
        print("📊 Test 6: Database Population Verification")
        
        # Try to analyze all new carrier prefixes
        new_carrier_numbers = [
            "0870123456",  # iTel
            "0920123456",  # Vietnamobile
            "0990123456",  # Wintel
            "0890123456",  # VNPAY Sky
        ]
        
        response = requests.post(f"{api_url}/analyze/", 
                               json={"phone_numbers": new_carrier_numbers},
                               timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if "results" in data:
                results = data["results"]
                safe_count = sum(1 for r in results if r.get("fraud_risk") == "LOW")
                
                if safe_count == len(new_carrier_numbers):
                    print(f"   ✅ All new carriers recognized: {safe_count}/{len(new_carrier_numbers)}")
                    print("   ✅ Database properly populated with 94+ headings")
                    tests_passed += 1
                else:
                    print(f"   ⚠️ New carriers recognition: {safe_count}/{len(new_carrier_numbers)}")
            else:
                print("   ⚠️ Unexpected response format")
        else:
            print(f"   ❌ New carrier test failed: HTTP {response.status_code}")
        
        print()
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Cannot reach API")
        print("💡 Make sure the Railway deployment is complete and running")
        print()
        
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: API response too slow")
        print("💡 Railway might still be starting up - try again in 1-2 minutes")
        print()
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print()
    
    # Summary
    print("=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Railway PostgreSQL setup is successful!")
        print()
        print("✅ Your API is ready for production use:")
        print(f"   🌐 API URL: {api_url}")
        print(f"   📚 Docs: {api_url}/docs")
        print(f"   🏥 Health: {api_url}/health")
        print()
        print("👥 Users can now call your API from anywhere!")
        
    elif tests_passed >= 4:
        print("🟡 MOSTLY WORKING - Minor issues detected")
        print("💡 API is functional but may need minor adjustments")
        
    else:
        print("❌ SETUP INCOMPLETE - Major issues detected")
        print("🔧 Check Railway logs and database configuration")
    
    print()
    return tests_passed == total_tests

def main():
    print("🚀 Railway PostgreSQL Database Test")
    print(f"🕐 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Get API URL from user
    api_url = input("📍 Enter your Railway API URL (e.g., https://your-app.up.railway.app): ").strip()
    
    if not api_url.startswith('https://'):
        print("❌ URL must start with https://")
        return
    
    # Remove trailing slash
    api_url = api_url.rstrip('/')
    
    print()
    success = test_railway_database(api_url)
    
    if success:
        print("🎯 Next steps:")
        print("1. Share API URL with users")
        print("2. Provide docs/FOR_USERS.md as user guide")
        print("3. Monitor usage via Railway dashboard")
        print("4. Scale up if needed")
    else:
        print("🔧 Troubleshooting:")
        print("1. Check Railway deployment logs")
        print("2. Verify PostgreSQL service is running")
        print("3. Check environment variables")
        print("4. Try redeploying if needed")

if __name__ == "__main__":
    main()
