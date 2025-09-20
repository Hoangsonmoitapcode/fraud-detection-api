#!/usr/bin/env python3
"""
Test script để tương tác với API Status endpoint
Chạy: python test_api_status.py
"""

import requests
import json
from datetime import datetime

def test_api_status():
    """Test API Status endpoint"""
    
    base_url = "http://localhost:8000"
    
    print("🔍 Testing API Status Endpoint...")
    print(f"📡 URL: {base_url}/")
    print("-" * 50)
    
    try:
        # Gửi GET request tới root endpoint
        response = requests.get(f"{base_url}/")
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"⏱️  Response Time: {response.elapsed.total_seconds():.3f}s")
        print()
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ API Status Response:")
            print("=" * 60)
            
            # Basic info
            print(f"🛡️  Message: {data.get('message')}")
            print(f"📋 Version: {data.get('version')}")
            print(f"🟢 Status: {data.get('status')}")
            print(f"🕐 Timestamp: {data.get('timestamp')}")
            print(f"⏰ Uptime: {data.get('uptime_seconds', 0):.2f} seconds")
            print()
            
            # System info
            if 'system_info' in data:
                print("💻 System Information:")
                sys_info = data['system_info']
                print(f"   🖥️  CPU Usage: {sys_info.get('cpu_usage', 'N/A')}")
                print(f"   🧠 Memory Usage: {sys_info.get('memory_usage', 'N/A')}")
                print()
            
            # Available endpoints
            if 'endpoints' in data:
                print("🌐 Available Endpoints:")
                endpoints = data['endpoints']
                for name, path in endpoints.items():
                    print(f"   📍 {name}: {base_url}{path}")
                print()
            
            # Features status
            if 'features' in data:
                print("🚀 Features Status:")
                features = data['features']
                for feature, status in features.items():
                    print(f"   {status} {feature}")
                print()
            
            # Full JSON response
            print("📄 Full JSON Response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error!")
        print("💡 Make sure the server is running:")
        print("   scripts\\start_server.bat")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health_endpoint():
    """Test Health Check endpoint"""
    
    base_url = "http://localhost:8000"
    
    print("\n" + "="*60)
    print("🏥 Testing Health Check Endpoint...")
    print(f"📡 URL: {base_url}/health")
    print("-" * 50)
    
    try:
        response = requests.get(f"{base_url}/health")
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"⏱️  Response Time: {response.elapsed.total_seconds():.3f}s")
        print()
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Health Check Response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Health status
            overall_status = data.get('status', 'unknown')
            if overall_status == 'healthy':
                print("\n🟢 System is HEALTHY!")
            elif overall_status == 'degraded':
                print("\n🟡 System is DEGRADED!")
            else:
                print(f"\n⚪ System status: {overall_status}")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error!")
        print("💡 Make sure the server is running")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 API Status & Health Check Test")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test API Status
    test_api_status()
    
    # Test Health Check
    test_health_endpoint()
    
    print("\n" + "="*60)
    print("✅ Test completed!")
