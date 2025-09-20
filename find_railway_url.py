#!/usr/bin/env python3
"""
Script to find Railway URL by testing common patterns
"""

import requests
import time

def test_railway_urls():
    """Test common Railway URL patterns"""
    
    # Common Railway URL patterns for your project
    possible_urls = [
        "https://fraud-detection-api-production.up.railway.app",
        "https://fraud-detection-api.up.railway.app", 
        "https://marvelous-flow.up.railway.app",
        "https://fraud-detection-api-production-marvelous-flow.up.railway.app",
        "https://hoangsonmoitapcode-fraud-detection-api.up.railway.app",
        "https://fraud-detection-api-production-28673fe1.up.railway.app"
    ]
    
    print("🔍 Searching for your Railway API URL...")
    print("=" * 60)
    
    working_urls = []
    
    for url in possible_urls:
        try:
            print(f"Testing: {url}")
            response = requests.get(f"{url}/health", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ FOUND! Working URL: {url}")
                working_urls.append(url)
                
                # Test API status too
                try:
                    status_response = requests.get(url, timeout=5)
                    if status_response.status_code == 200:
                        data = status_response.json()
                        version = data.get("version", "unknown")
                        print(f"   📊 API Version: {version}")
                        print(f"   🌐 API Docs: {url}/docs")
                except:
                    pass
                    
                print()
            else:
                print(f"❌ Not working: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection failed")
        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(0.5)  # Be nice to Railway
    
    print("=" * 60)
    
    if working_urls:
        print(f"🎉 Found {len(working_urls)} working URL(s):")
        for url in working_urls:
            print(f"   🌐 {url}")
            print(f"   📚 Docs: {url}/docs")
            print(f"   🏥 Health: {url}/health")
        
        print("\n🚀 Next steps:")
        print("1. Use any of the URLs above")
        print("2. Setup database with admin endpoint")
        print("3. Test phone analysis")
        
        return working_urls[0]  # Return first working URL
    else:
        print("❌ No working URLs found")
        print("\n🔧 Troubleshooting:")
        print("1. Check Railway dashboard for actual URL")
        print("2. Ensure deployment is successful")
        print("3. Check if service is running")
        print("4. Generate domain if not exists")
        
        return None

if __name__ == "__main__":
    print("🚀 Railway URL Finder")
    print(f"🕐 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    url = test_railway_urls()
    
    if url:
        print(f"\n🎯 Your API URL: {url}")
        print("\nReady to setup database? Run:")
        print(f'curl -X POST "{url}/admin/setup-database"')
    else:
        print("\n💡 Please check Railway dashboard manually for the correct URL")
        print("Look for: Service → Settings → Domains")
