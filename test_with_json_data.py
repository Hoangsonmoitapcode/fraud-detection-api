#!/usr/bin/env python3
"""
Test script using JSON data files
"""
import requests
import json
import os

def load_json_data(filename):
    """Load JSON data from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File {filename} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {filename}: {e}")
        return None

def test_websites_from_json(base_url: str = "http://localhost:8000"):
    """Test website scam reporting using JSON data"""
    
    print("🌐 Testing Websites from JSON Data")
    print("=" * 50)
    
    # Load test data
    data = load_json_data("test_data_websites.json")
    if not data:
        return
    
    try:
        response = requests.post(
            f"{base_url}/website-scam/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result.get("summary", {})
            results = result.get("results", [])
            
            print(f"✅ SUCCESS")
            print(f"   Total submitted: {summary.get('total_submitted')}")
            print(f"   Created: {summary.get('created_count')}")
            print(f"   Updated: {summary.get('updated_count')}")
            print(f"   Duplicates: {summary.get('duplicate_count')}")
            print(f"   Errors: {summary.get('error_count')}")
            
            # Count by label
            scam_count = len([r for r in results if r.get('status') == 'created' and 'scam' in str(r.get('website_url', ''))])
            safe_count = len([r for r in results if r.get('status') == 'created' and any(safe_site in str(r.get('website_url', '')) for safe_site in ['google.com', 'github.com', 'stackoverflow.com', 'microsoft.com'])])
            
            print(f"   Breakdown:")
            print(f"     🔴 Scam sites: {len([w for w in data['websites'] if w['label'] == 'scam'])}")
            print(f"     🟢 Safe sites: {len([w for w in data['websites'] if w['label'] == 'safe'])}")
            
            # Show sample results
            print(f"   Sample results:")
            for i, result in enumerate(results[:5]):
                status_icon = {"created": "✅", "updated": "🔄", "duplicate": "↩️", "error": "❌"}.get(result.get("status"), "❓")
                url = result.get("website_url", "")[:50] + "..." if len(result.get("website_url", "")) > 50 else result.get("website_url", "")
                label = result.get("label", "unknown")
                label_icon = "🔴" if label == "scam" else "🟢"
                print(f"     {status_icon} {label_icon} {url}")
                
            if len(results) > 5:
                print(f"     ... and {len(results) - 5} more")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_banking_from_json(base_url: str = "http://localhost:8000"):
    """Test banking scam reporting using JSON data"""
    
    print("\n🏦 Testing Banking from JSON Data")
    print("=" * 50)
    
    # Load test data
    data = load_json_data("test_data_banking.json")
    if not data:
        return
    
    try:
        response = requests.post(
            f"{base_url}/banking-scam/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result.get("summary", {})
            results = result.get("results", [])
            
            print(f"✅ SUCCESS")
            print(f"   Total submitted: {summary.get('total_submitted')}")
            print(f"   Created: {summary.get('created_count')}")
            print(f"   Duplicates: {summary.get('duplicate_count')}")
            print(f"   Errors: {summary.get('error_count')}")
            
            # Count by bank
            bank_counts = {}
            for account in data['banking_accounts']:
                bank = account['bank_name']
                bank_counts[bank] = bank_counts.get(bank, 0) + 1
            
            print(f"   Banks breakdown:")
            for bank, count in sorted(bank_counts.items()):
                print(f"     🏛️  {bank}: {count} accounts")
            
            # Show sample results
            print(f"   Sample results:")
            for i, result in enumerate(results[:5]):
                status_icon = {"created": "✅", "duplicate": "🔄", "error": "❌"}.get(result.get("status"), "❓")
                account = result.get("account_number", "")
                bank = result.get("bank_name", "")
                print(f"     {status_icon} {account} @ {bank}")
                
            if len(results) > 5:
                print(f"     ... and {len(results) - 5} more")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_duplicate_detection(base_url: str = "http://localhost:8000"):
    """Test duplicate detection by running same data twice"""
    
    print("\n🔄 Testing Duplicate Detection")
    print("=" * 50)
    
    # Test with smaller dataset for duplicate detection
    small_website_data = {
        "websites": [
            {"website_url": "https://duplicate-test-site.com", "label": "scam"},
            {"website_url": "https://another-duplicate-test.org", "label": "scam"}
        ]
    }
    
    print("   First submission (should create)...")
    try:
        response1 = requests.post(f"{base_url}/website-scam/", json=small_website_data, headers={"Content-Type": "application/json"})
        if response1.status_code == 200:
            data1 = response1.json()
            created1 = data1.get("summary", {}).get("created_count", 0)
            print(f"   ✅ Created: {created1}")
        
        print("   Second submission (should detect duplicates)...")
        response2 = requests.post(f"{base_url}/website-scam/", json=small_website_data, headers={"Content-Type": "application/json"})
        if response2.status_code == 200:
            data2 = response2.json()
            created2 = data2.get("summary", {}).get("created_count", 0)
            duplicates2 = data2.get("summary", {}).get("duplicate_count", 0)
            
            print(f"   ✅ Created: {created2}, Duplicates: {duplicates2}")
            
            if duplicates2 > 0 and created2 == 0:
                print(f"   🎉 Duplicate detection working perfectly!")
            else:
                print(f"   ⚠️  Unexpected duplicate handling")
                
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def show_json_file_contents():
    """Show the contents of JSON files for reference"""
    
    print("\n📄 JSON Test Data Files")
    print("=" * 50)
    
    print("   Website data (test_data_websites.json):")
    data = load_json_data("test_data_websites.json")
    if data:
        websites = data.get('websites', [])
        scam_sites = [w for w in websites if w['label'] == 'scam']
        safe_sites = [w for w in websites if w['label'] == 'safe']
        
        print(f"     Total websites: {len(websites)}")
        print(f"     Scam sites: {len(scam_sites)}")
        print(f"     Safe sites: {len(safe_sites)}")
        
        print(f"     Sample scam sites:")
        for site in scam_sites[:3]:
            print(f"       🔴 {site['website_url']}")
            
        print(f"     Sample safe sites:")
        for site in safe_sites[:3]:
            print(f"       🟢 {site['website_url']}")
    
    print("\n   Banking data (test_data_banking.json):")
    data = load_json_data("test_data_banking.json")
    if data:
        accounts = data.get('banking_accounts', [])
        banks = list(set(acc['bank_name'] for acc in accounts))
        
        print(f"     Total accounts: {len(accounts)}")
        print(f"     Unique banks: {len(banks)}")
        print(f"     Banks: {', '.join(sorted(banks))}")
        
        print(f"     Sample accounts:")
        for acc in accounts[:3]:
            print(f"       🏦 {acc['account_number']} @ {acc['bank_name']}")

if __name__ == "__main__":
    print("🚀 Testing with JSON Data Files...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("This will CREATE RECORDS in your database!")
    print("\n" + "=" * 80)
    
    # Show file contents first
    show_json_file_contents()
    
    # Run tests
    test_websites_from_json()
    test_banking_from_json()
    test_duplicate_detection()
    
    print("\n" + "=" * 80)
    print("🏁 JSON data testing completed!")
    print("\n📝 Usage:")
    print("   curl -X POST 'http://localhost:8000/website-scam/' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d @test_data_websites.json")
    print("")
    print("   curl -X POST 'http://localhost:8000/banking-scam/' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d @test_data_banking.json")
