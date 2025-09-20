#!/usr/bin/env python3
"""
Test unified batch endpoints - single or multiple items
"""
import requests
import json

def test_banking_scam_unified(base_url: str = "http://localhost:8000"):
    """Test banking scam endpoint with single and batch data"""
    
    print("🏦 Testing Unified Banking Scam Endpoint")
    print("=" * 50)
    
    # Test 1: Single account
    print("\n🔹 Testing Single Account")
    single_request = {
        "banking_accounts": [
            {"account_number": "1111111111", "bank_name": "Test Bank Single"}
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/banking-scam/",
            json=single_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", {})
            print(f"✅ SUCCESS - Single account")
            print(f"   Created: {summary.get('created_count')}")
            print(f"   Results: {len(data.get('results', []))}")
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")
    
    # Test 2: Multiple accounts
    print("\n🔹 Testing Multiple Accounts")
    batch_request = {
        "banking_accounts": [
            {"account_number": "2222222222", "bank_name": "Test Bank Multi 1"},
            {"account_number": "3333333333", "bank_name": "Test Bank Multi 2"},
            {"account_number": "4444444444", "bank_name": "Test Bank Multi 3"}
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/banking-scam/",
            json=batch_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", {})
            print(f"✅ SUCCESS - Multiple accounts")
            print(f"   Total submitted: {summary.get('total_submitted')}")
            print(f"   Created: {summary.get('created_count')}")
            print(f"   Duplicates: {summary.get('duplicate_count')}")
            
            # Show results
            results = data.get("results", [])
            for result in results:
                status_icon = {"created": "✅", "duplicate": "🔄", "error": "❌"}.get(result.get("status"), "❓")
                print(f"   {status_icon} {result.get('account_number')} @ {result.get('bank_name')} → {result.get('status')}")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_website_scam_unified(base_url: str = "http://localhost:8000"):
    """Test website scam endpoint with single and batch data"""
    
    print("\n🌐 Testing Unified Website Scam Endpoint")
    print("=" * 50)
    
    # Test 1: Single website
    print("\n🔹 Testing Single Website")
    single_request = {
        "websites": [
            {"website_url": "https://single-scam-site.com", "label": "scam"}
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/website-scam/",
            json=single_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", {})
            print(f"✅ SUCCESS - Single website")
            print(f"   Created: {summary.get('created_count')}")
            print(f"   Updated: {summary.get('updated_count')}")
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")
    
    # Test 2: Multiple websites
    print("\n🔹 Testing Multiple Websites")
    batch_request = {
        "websites": [
            {"website_url": "https://batch-scam-site-1.com", "label": "scam"},
            {"website_url": "https://batch-scam-site-2.org", "label": "scam"},
            {"website_url": "https://legitimate-site.com", "label": "safe"}
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/website-scam/",
            json=batch_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", {})
            print(f"✅ SUCCESS - Multiple websites")
            print(f"   Total submitted: {summary.get('total_submitted')}")
            print(f"   Created: {summary.get('created_count')}")
            print(f"   Updated: {summary.get('updated_count')}")
            print(f"   Duplicates: {summary.get('duplicate_count')}")
            
            # Show results
            results = data.get("results", [])
            for result in results:
                status_icon = {"created": "✅", "updated": "🔄", "duplicate": "↩️", "error": "❌"}.get(result.get("status"), "❓")
                url = result.get("website_url", "")[:50] + "..." if len(result.get("website_url", "")) > 50 else result.get("website_url", "")
                print(f"   {status_icon} {url} ({result.get('label')}) → {result.get('status')}")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_sms_scam_unified(base_url: str = "http://localhost:8000"):
    """Test SMS scam endpoint with single and batch data"""
    
    print("\n📱 Testing Unified SMS Scam Endpoint")
    print("=" * 50)
    
    # Test 1: Single SMS
    print("\n🔹 Testing Single SMS")
    single_request = {
        "sms_messages": [
            {"sms_content": "Single SMS test: Chúc mừng bạn trúng thưởng 50 triệu!", "label": "spam"}
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/sms-scam/",
            json=single_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", {})
            print(f"✅ SUCCESS - Single SMS")
            print(f"   Created: {summary.get('created_count')}")
            print(f"   Updated: {summary.get('updated_count')}")
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")
    
    # Test 2: Multiple SMS
    print("\n🔹 Testing Multiple SMS")
    batch_request = {
        "sms_messages": [
            {"sms_content": "Batch SMS 1: Tài khoản của bạn sẽ bị khóa, truy cập link ngay!", "label": "spam"},
            {"sms_content": "Batch SMS 2: Cuộc họp team lúc 3pm hôm nay tại phòng A1", "label": "safe"},
            {"sms_content": "Batch SMS 3: KHẨN CẤP! Xác minh thông tin để nhận 100 triệu", "label": "spam"}
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/sms-scam/",
            json=batch_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", {})
            print(f"✅ SUCCESS - Multiple SMS")
            print(f"   Total submitted: {summary.get('total_submitted')}")
            print(f"   Created: {summary.get('created_count')}")
            print(f"   Updated: {summary.get('updated_count')}")
            print(f"   Duplicates: {summary.get('duplicate_count')}")
            
            # Show results
            results = data.get("results", [])
            for result in results:
                status_icon = {"created": "✅", "updated": "🔄", "duplicate": "↩️", "error": "❌"}.get(result.get("status"), "❓")
                content = result.get("sms_content", "")
                print(f"   {status_icon} {content[:50]}... ({result.get('label')}) → {result.get('status')}")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_duplicate_handling(base_url: str = "http://localhost:8000"):
    """Test duplicate handling across all endpoints"""
    
    print("\n🔄 Testing Duplicate Handling")
    print("=" * 50)
    
    # Test duplicate banking accounts
    print("\n🔹 Testing Banking Duplicates")
    duplicate_banking = {
        "banking_accounts": [
            {"account_number": "9999999999", "bank_name": "Duplicate Test Bank"}
        ]
    }
    
    # First submission
    try:
        response1 = requests.post(f"{base_url}/banking-scam/", json=duplicate_banking, headers={"Content-Type": "application/json"})
        if response1.status_code == 200:
            data1 = response1.json()
            created1 = data1.get("summary", {}).get("created_count", 0)
            print(f"   First submission: {created1} created")
        
        # Second submission (should be duplicate)
        response2 = requests.post(f"{base_url}/banking-scam/", json=duplicate_banking, headers={"Content-Type": "application/json"})
        if response2.status_code == 200:
            data2 = response2.json()
            duplicates2 = data2.get("summary", {}).get("duplicate_count", 0)
            print(f"   Second submission: {duplicates2} duplicates (✅ if 1)")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Unified Batch Endpoints Tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("This will CREATE RECORDS in your database!")
    print("\n" + "=" * 80)
    
    # Run tests
    test_banking_scam_unified()
    test_website_scam_unified()
    test_sms_scam_unified()
    test_duplicate_handling()
    
    print("\n" + "=" * 80)
    print("🏁 Unified batch endpoints testing completed!")
    print("\n🎉 Key Benefits:")
    print("   ✅ Single endpoint handles 1 or multiple items")
    print("   ✅ Consistent response format")
    print("   ✅ Better error handling")
    print("   ✅ Duplicate detection")
    print("   ✅ Cleaner API design")
