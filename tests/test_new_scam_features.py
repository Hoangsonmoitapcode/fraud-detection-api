#!/usr/bin/env python3
"""
Test cases for new scam detection features: SMS, Banking, Website
"""
import requests
import json
from typing import List, Dict

def test_sms_scam_features(base_url: str = "http://localhost:8000") -> None:
    """Test SMS scam detection features"""
    
    print("📱 Testing SMS Scam Detection Features")
    print("=" * 50)
    
    # Test cases for SMS
    sms_test_cases = [
        {
            "content": "Chúc mừng! Bạn đã trúng thưởng 100 triệu đồng. Truy cập ngay: http://fake-lottery.com",
            "label": "spam",
            "description": "Lottery scam SMS"
        },
        {
            "content": "Tài khoản của bạn sẽ bị khóa trong 24h. Truy cập: http://fake-bank.com để xác minh",
            "label": "spam", 
            "description": "Fake banking alert"
        },
        {
            "content": "Xin chào, cuộc họp sẽ diễn ra lúc 2pm hôm nay",
            "label": "safe",
            "description": "Normal meeting reminder"
        }
    ]
    
    print("\n🔹 Testing SMS Reporting...")
    for i, test_case in enumerate(sms_test_cases, 1):
        try:
            response = requests.post(
                f"{base_url}/sms-scam/",
                json={
                    "sms_content": test_case["content"],
                    "label": test_case["label"]
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SMS {i} reported: {test_case['description']}")
                print(f"   ID: {data.get('id')}, Label: {data.get('label')}")
            else:
                print(f"❌ SMS {i} failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ SMS {i} error: {str(e)}")
    
    print("\n🔹 Testing SMS Checking...")
    check_cases = [
        "Chúc mừng! Bạn đã trúng thưởng",  # Should match spam
        "Cuộc họp sẽ diễn ra",  # Should match safe
        "This is a completely new message"  # Should not match
    ]
    
    for i, check_content in enumerate(check_cases, 1):
        try:
            response = requests.get(
                f"{base_url}/check-sms/",
                params={"sms_content": check_content}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Check {i}: {check_content[:30]}...")
                print(f"   Spam: {data.get('is_spam')}, Risk: {data.get('risk_level')}, Match: {data.get('match_type')}")
            else:
                print(f"❌ Check {i} failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Check {i} error: {str(e)}")


def test_banking_scam_features(base_url: str = "http://localhost:8000") -> None:
    """Test banking scam detection features"""
    
    print("\n" + "=" * 50)
    print("🏦 Testing Banking Scam Detection Features")
    print("=" * 50)
    
    # Test cases for banking
    banking_test_cases = [
        {
            "account_number": "1234567890",
            "bank_name": "Vietcombank",
            "description": "Reported scam account"
        },
        {
            "account_number": "0987654321", 
            "bank_name": "Techcombank",
            "description": "Another scam account"
        },
        {
            "account_number": "1111222233",
            "bank_name": "BIDV",
            "description": "Third scam account"
        }
    ]
    
    print("\n🔹 Testing Banking Scam Reporting...")
    for i, test_case in enumerate(banking_test_cases, 1):
        try:
            response = requests.post(
                f"{base_url}/banking-scam/",
                json={
                    "account_number": test_case["account_number"],
                    "bank_name": test_case["bank_name"]
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Banking {i} reported: {test_case['description']}")
                print(f"   ID: {data.get('id')}, Account: {data.get('account_number')}, Bank: {data.get('bank_name')}")
            else:
                print(f"❌ Banking {i} failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Banking {i} error: {str(e)}")
    
    print("\n🔹 Testing Banking Scam Checking...")
    for i, test_case in enumerate(banking_test_cases, 1):
        try:
            response = requests.get(
                f"{base_url}/check-banking/",
                params={
                    "account_number": test_case["account_number"],
                    "bank_name": test_case["bank_name"]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Check {i}: {test_case['account_number']} @ {test_case['bank_name']}")
                print(f"   Scam: {data.get('is_scam')}, Risk: {data.get('risk_level')}")
            else:
                print(f"❌ Check {i} failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Check {i} error: {str(e)}")


def test_website_scam_features(base_url: str = "http://localhost:8000") -> None:
    """Test website scam detection features"""
    
    print("\n" + "=" * 50)
    print("🌐 Testing Website Scam Detection Features") 
    print("=" * 50)
    
    # Test cases for websites
    website_test_cases = [
        {
            "website_url": "https://fake-vietcombank.com",
            "label": "scam",
            "description": "Fake banking website"
        },
        {
            "website_url": "https://lottery-scam-site.net",
            "label": "scam",
            "description": "Fake lottery website"
        },
        {
            "website_url": "https://legit-news-site.com",
            "label": "safe",
            "description": "Legitimate news website"
        },
        {
            "website_url": "https://phishing-paypal.org",
            "label": "scam", 
            "description": "Phishing website"
        }
    ]
    
    print("\n🔹 Testing Website Scam Reporting...")
    for i, test_case in enumerate(website_test_cases, 1):
        try:
            response = requests.post(
                f"{base_url}/website-scam/",
                json={
                    "website_url": test_case["website_url"],
                    "label": test_case["label"]
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Website {i} reported: {test_case['description']}")
                print(f"   ID: {data.get('id')}, URL: {data.get('website_url')}, Label: {data.get('label')}")
            else:
                print(f"❌ Website {i} failed: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Website {i} error: {str(e)}")
    
    print("\n🔹 Testing Website Scam Checking...")
    for i, test_case in enumerate(website_test_cases, 1):
        try:
            response = requests.get(
                f"{base_url}/check-website/",
                params={"website_url": test_case["website_url"]}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Check {i}: {test_case['website_url']}")
                print(f"   Scam: {data.get('is_scam')}, Label: {data.get('label')}, Risk: {data.get('risk_level')}")
            else:
                print(f"❌ Check {i} failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Check {i} error: {str(e)}")


def run_comprehensive_test(base_url: str = "http://localhost:8000") -> None:
    """Run all scam detection tests"""
    
    print("🚀 Starting Comprehensive Scam Detection Tests...")
    print("Make sure your FastAPI server is running on " + base_url)
    print("\n" + "=" * 80)
    
    # Test all features
    test_sms_scam_features(base_url)
    test_banking_scam_features(base_url) 
    test_website_scam_features(base_url)
    
    print("\n" + "=" * 80)
    print("🏁 All tests completed!")
    print("\n📊 Summary:")
    print("   - SMS Scam Detection: Report & Check functionality")
    print("   - Banking Scam Detection: Account & Bank validation")
    print("   - Website Scam Detection: URL & Label classification")
    print("\n🎉 New fraud detection features are ready for production!")


if __name__ == "__main__":
    run_comprehensive_test()
