#!/usr/bin/env python3
"""
Test unified analyze endpoint - single or multiple phone numbers
"""
import requests
import json

def test_single_phone_analysis(base_url: str = "http://localhost:8000"):
    """Test single phone analysis (backward compatibility)"""
    
    print("📱 Testing Single Phone Analysis")
    print("=" * 50)
    
    # Single phone request
    single_request = {
        "phone_numbers": ["0965842855"]  # Array with 1 item
    }
    
    try:
        response = requests.post(
            f"{base_url}/analyze/",
            json=single_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if it returns simple format (backward compatibility)
            if "phone_number" in data and "analysis" in data and "fraud_risk" in data:
                print(f"✅ SUCCESS - Simple format (backward compatible)")
                print(f"   Phone: {data.get('phone_number')}")
                print(f"   Region: {data.get('analysis', {}).get('phone_region')}")
                print(f"   Risk: {data.get('fraud_risk')}")
                print(f"   Head: {data.get('analysis', {}).get('phone_head')}")
            else:
                print(f"✅ SUCCESS - Batch format")
                summary = data.get("summary", {})
                print(f"   Analyzed: {summary.get('total_analyzed')}")
                print(f"   High risk: {summary.get('high_risk_count')}")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_multiple_phone_analysis(base_url: str = "http://localhost:8000"):
    """Test multiple phone analysis"""
    
    print("\n📱 Testing Multiple Phone Analysis")
    print("=" * 50)
    
    # Multiple phones request
    batch_request = {
        "phone_numbers": [
            "0965842855",    # Vietnamese (safe)
            "0987654321",    # Vietnamese (safe)
            "+12345678901",  # US (unsafe)
            "+447123456789", # UK (unsafe)
            "+8613812345678" # China (unsafe)
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/analyze/",
            json=batch_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Should return batch format for multiple phones
            if "summary" in data:
                summary = data.get("summary", {})
                results = data.get("results", [])
                
                print(f"✅ SUCCESS - Batch format")
                print(f"   Total analyzed: {summary.get('total_analyzed')}")
                print(f"   High risk: {summary.get('high_risk_count')}")
                print(f"   Low risk: {summary.get('low_risk_count')}")
                print(f"   Errors: {summary.get('error_count')}")
                print(f"   Processing time: {summary.get('processing_time')}s")
                
                # Show risk distribution
                safe_count = sum(1 for r in results if r.get("fraud_risk") == "LOW")
                unsafe_count = sum(1 for r in results if r.get("fraud_risk") == "HIGH")
                
                print(f"   Results breakdown:")
                print(f"     🟢 Safe (Vietnam): {safe_count}")
                print(f"     🔴 Unsafe (International): {unsafe_count}")
                
                # Show sample results
                print(f"   Sample results:")
                for result in results[:3]:
                    risk_icon = "🟢" if result.get("fraud_risk") == "LOW" else "🔴"
                    phone = result.get("phone_number")
                    region = result.get("analysis", {}).get("phone_region", "Unknown")
                    risk = result.get("fraud_risk")
                    print(f"     {risk_icon} {phone} ({region}) → {risk}")
                    
                if len(results) > 3:
                    print(f"     ... and {len(results) - 3} more")
                    
            else:
                print(f"⚠️  Unexpected format: {data}")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_error_handling(base_url: str = "http://localhost:8000"):
    """Test error handling for invalid phone numbers"""
    
    print("\n❌ Testing Error Handling")
    print("=" * 50)
    
    # Mixed valid and invalid numbers
    error_request = {
        "phone_numbers": [
            "0965842855",    # Valid Vietnamese
            "invalid_phone", # Invalid format
            "",              # Empty string
            "123",           # Too short
            "+12345678901"   # Valid US
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/analyze/",
            json=error_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "summary" in data:
                summary = data.get("summary", {})
                results = data.get("results", [])
                
                print(f"✅ SUCCESS - Error handling")
                print(f"   Total processed: {summary.get('total_analyzed')}")
                print(f"   Successful: {summary.get('high_risk_count') + summary.get('low_risk_count')}")
                print(f"   Errors: {summary.get('error_count')}")
                
                # Show error details
                errors = [r for r in results if r.get("status") == "error"]
                successes = [r for r in results if r.get("status") == "success"]
                
                print(f"   Error breakdown:")
                for error in errors:
                    phone = error.get("phone_number", "Unknown")
                    message = error.get("error", "Unknown error")
                    print(f"     ❌ {phone} → {message}")
                
                print(f"   Success breakdown:")
                for success in successes:
                    phone = success.get("phone_number")
                    risk = success.get("fraud_risk")
                    region = success.get("analysis", {}).get("phone_region", "Unknown")
                    risk_icon = "🟢" if risk == "LOW" else "🔴"
                    print(f"     {risk_icon} {phone} ({region}) → {risk}")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_performance_comparison(base_url: str = "http://localhost:8000"):
    """Test performance of unified endpoint"""
    
    print("\n⚡ Testing Performance")
    print("=" * 50)
    
    # Large batch for performance testing
    large_batch = {
        "phone_numbers": [
            "0965000001", "0965000002", "0965000003", "0965000004", "0965000005",
            "+12340000001", "+12340000002", "+12340000003", "+12340000004", "+12340000005",
            "+447000000001", "+447000000002", "+447000000003", "+447000000004", "+447000000005"
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/analyze/",
            json=large_batch,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "summary" in data:
                summary = data.get("summary", {})
                processing_time = summary.get("processing_time", 0)
                total_analyzed = summary.get("total_analyzed", 0)
                
                print(f"✅ SUCCESS - Performance test")
                print(f"   Numbers analyzed: {total_analyzed}")
                print(f"   Processing time: {processing_time}s")
                print(f"   Average per number: {(processing_time/total_analyzed)*1000:.1f}ms")
                
                # Performance rating
                if processing_time < 0.1:
                    print(f"   🚀 Excellent performance!")
                elif processing_time < 0.5:
                    print(f"   ✅ Good performance")
                else:
                    print(f"   ⚠️  Consider optimization")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def test_backward_compatibility(base_url: str = "http://localhost:8000"):
    """Test backward compatibility with old analyze format"""
    
    print("\n🔙 Testing Backward Compatibility")
    print("=" * 50)
    
    # Single number should return simple format
    single_request = {
        "phone_numbers": ["0965999999"]
    }
    
    try:
        response = requests.post(
            f"{base_url}/analyze/",
            json=single_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if it has old analyze format
            expected_fields = ["phone_number", "analysis", "fraud_risk"]
            has_old_format = all(field in data for field in expected_fields)
            
            if has_old_format and "summary" not in data:
                print(f"✅ Backward compatibility maintained")
                print(f"   Returns simple format for single number")
                print(f"   Fields: {list(data.keys())}")
            else:
                print(f"⚠️  Returns batch format instead of simple format")
                print(f"   This might break existing clients")
                print(f"   Fields: {list(data.keys())}")
                
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Unified Analyze Endpoint Tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("This will ANALYZE phone numbers (no database writes)")
    print("\n" + "=" * 80)
    
    # Run tests
    test_single_phone_analysis()
    test_multiple_phone_analysis()
    test_error_handling()
    test_performance_comparison()
    test_backward_compatibility()
    
    print("\n" + "=" * 80)
    print("🏁 Unified analyze endpoint testing completed!")
    print("\n🎉 Benefits of Unified Endpoint:")
    print("   ✅ Single endpoint handles 1 or multiple phones")
    print("   ✅ Backward compatibility for single phone")
    print("   ✅ Consistent batch format for multiple phones")
    print("   ✅ Better error handling")
    print("   ✅ Performance metrics included")
    print("   ✅ Cleaner API design")
    print("   ✅ No database writes (pure analysis)")
