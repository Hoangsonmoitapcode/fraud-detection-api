#!/usr/bin/env python3
"""
Test script for new model loading workflow on Railway deployment
Uses separate load-model and predict-sms endpoints
"""

import requests
import json
import time

# Railway domain - update this with your actual domain
DOMAIN = "https://frauddetection-production-a35d.up.railway.app"

def test_ping():
    """Test basic connectivity"""
    print("🏓 Testing ping endpoint...")
    try:
        response = requests.get(f"{DOMAIN}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ping failed: {e}")
        return False

def test_load_model():
    """Test manual model loading endpoint - takes 2-3 minutes"""
    print("\n🚀 Testing manual model loading...")
    print("⏳ This may take 2-3 minutes on free plan...")
    try:
        start_time = time.time()
        response = requests.post(f"{DOMAIN}/load-model", timeout=300)  # 5 minute timeout
        load_time = time.time() - start_time
        
        print(f"Status: {response.status_code}")
        print(f"Load time: {load_time:.1f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            print(f"📝 Message: {data.get('message')}")
            print(f"🔍 Model loaded: {data.get('model_info', {}).get('is_loaded', False)}")
            print(f"🔄 Fallback mode: {data.get('model_info', {}).get('fallback_mode', False)}")
            print(f"🏷️ Model type: {data.get('model_info', {}).get('model_type', 'Unknown')}")
            
            if 'test_prediction' in data:
                print(f"🧪 Test prediction: {data['test_prediction']}")
            
            return data.get('status') == 'success'
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_model_status():
    """Test model status endpoint"""
    print("\n📊 Testing model status...")
    try:
        response = requests.get(f"{DOMAIN}/model-status")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Model loaded: {data.get('model_info', {}).get('is_loaded', False)}")
            print(f"Fallback mode: {data.get('model_info', {}).get('fallback_mode', False)}")
            print(f"Model type: {data.get('model_info', {}).get('model_type', 'Unknown')}")
            return data
        else:
            print(f"❌ Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Model status test failed: {e}")
        return None

def test_prediction(sms_text: str):
    """Test SMS prediction after model is loaded"""
    print(f"\n🔮 Testing prediction for: '{sms_text}'")
    try:
        start_time = time.time()
        response = requests.post(
            f"{DOMAIN}/predict-sms/", 
            json={"sms_content": sms_text},
            timeout=30
        )
        prediction_time = time.time() - start_time
        
        print(f"Status: {response.status_code}")
        print(f"Prediction time: {prediction_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction: {data.get('prediction')}")
            print(f"🎯 Confidence: {data.get('confidence', 0):.3f}")
            print(f"🏷️ Risk level: {data.get('risk_level')}")
            print(f"⚙️ Method: {data.get('model_info', {}).get('method', 'unknown')}")
            return True
        else:
            print(f"❌ Prediction error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

def main():
    """Main test workflow"""
    print("🧪 NEW MODEL LOADING WORKFLOW TEST")
    print("="*50)
    
    # Step 1: Test connectivity
    if not test_ping():
        print("❌ Basic connectivity failed. Stopping tests.")
        return
    
    # Step 2: Check initial model status
    test_model_status()
    
    # Step 3: Load model manually (2-3 minutes)
    print("\n" + "="*50)
    print("⚠️ STEP 3: MANUAL MODEL LOADING")
    print("This is the new workflow - load model first, then predict")
    print("="*50)
    
    model_loaded = test_load_model()
    
    if not model_loaded:
        print("❌ Model loading failed. Testing predictions anyway (will likely fail)...")
    
    # Step 4: Check model status after loading
    print("\n" + "="*50)
    print("📊 STEP 4: POST-LOAD MODEL STATUS")
    print("="*50)
    test_model_status()
    
    # Step 5: Test predictions (should be fast now)
    print("\n" + "="*50)
    print("🔮 STEP 5: FAST PREDICTIONS (Model Pre-loaded)")
    print("="*50)
    
    test_cases = [
        "Congratulations! You won $10000! Click here to claim your prize!",
        "Hey, are you coming to the meeting tomorrow?",
        "FREE MONEY!!! Click now to claim your cash prize!!!",
        "Mom called, please call her back when you get this"
    ]
    
    for test_sms in test_cases:
        test_prediction(test_sms)
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "="*50)
    print("✅ TEST COMPLETED")
    print("="*50)

if __name__ == "__main__":
    main()
