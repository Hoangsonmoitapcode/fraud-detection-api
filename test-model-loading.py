#!/usr/bin/env python3
"""
Test script to trigger model loading on Railway deployment
"""

import requests
import json
import time

# Replace with your actual Railway domain from the docs
DOMAIN = "https://fraud-detection-api-copy-copy-co.up.railway.app"

def test_model_loading():
    print("🧪 Testing Model Loading on Railway...")
    
    # 1. Test basic connectivity
    print("\n1. Testing basic connectivity...")
    try:
        response = requests.get(f"{DOMAIN}/ping", timeout=10)
        print(f"   ✅ Ping: {response.json()}")
    except Exception as e:
        print(f"   ❌ Ping failed: {e}")
        return
    
    # 2. Check initial model status
    print("\n2. Checking initial model status...")
    try:
        response = requests.get(f"{DOMAIN}/model-status", timeout=10)
        model_status = response.json()
        print(f"   📊 Model loaded: {model_status['model_info']['is_loaded']}")
        print(f"   📊 Fallback mode: {model_status['model_info']['fallback_mode']}")
    except Exception as e:
        print(f"   ⚠️ Model status check failed: {e}")
    
    # 3. Trigger model loading with prediction
    print("\n3. Triggering model loading with SMS prediction...")
    test_sms = "Congratulations! You won $10000! Click here to claim your prize!"
    
    try:
        print("   ⏳ Sending prediction request (this may take 2-3 minutes for first load)...")
        start_time = time.time()
        
        response = requests.post(
            f"{DOMAIN}/predict-sms/",
            json={"sms_content": test_sms},
            timeout=300  # 5 minutes timeout for model loading
        )
        
        load_time = time.time() - start_time
        result = response.json()
        
        print(f"   ✅ Prediction completed in {load_time:.1f} seconds")
        print(f"   🤖 Prediction: {result['prediction']}")
        print(f"   📈 Confidence: {result['confidence']:.2f}")
        print(f"   🔧 Method: {result.get('model_info', {}).get('method', 'unknown')}")
        
    except Exception as e:
        print(f"   ❌ Prediction failed: {e}")
        return
    
    # 4. Check model status after loading
    print("\n4. Checking model status after loading...")
    try:
        response = requests.get(f"{DOMAIN}/model-status", timeout=10)
        model_status = response.json()
        print(f"   📊 Model loaded: {model_status['model_info']['is_loaded']}")
        print(f"   📊 Fallback mode: {model_status['model_info']['fallback_mode']}")
        print(f"   📊 Model type: {model_status['model_info']['model_type']}")
    except Exception as e:
        print(f"   ⚠️ Model status check failed: {e}")
    
    # 5. Test second prediction (should be fast)
    print("\n5. Testing second prediction (should be fast)...")
    try:
        start_time = time.time()
        response = requests.post(
            f"{DOMAIN}/predict-sms/",
            json={"sms_content": "Hello, how are you today?"},
            timeout=30
        )
        load_time = time.time() - start_time
        result = response.json()
        
        print(f"   ⚡ Second prediction: {load_time:.2f} seconds")
        print(f"   🤖 Prediction: {result['prediction']}")
        print(f"   📈 Confidence: {result['confidence']:.2f}")
        
    except Exception as e:
        print(f"   ❌ Second prediction failed: {e}")
    
    print("\n🎉 Model loading test completed!")
    print(f"📱 Your API is ready at: {DOMAIN}")

if __name__ == "__main__":
    print("🚀 Fraud Detection API - Model Loading Test")
    print("=" * 50)
    
    # You need to update the DOMAIN variable above
    if DOMAIN == "https://your-domain.railway.app":
        print("⚠️ Please update the DOMAIN variable in this script with your actual Railway domain!")
    else:
        test_model_loading()
