#!/usr/bin/env python3
"""
Load trained model from models/trained/ folder and test it
"""

import torch
import os
import sys
import json
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pickle

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def load_trained_model(model_folder_path="models/trained"):
    """
    Load trained model from folder containing:
    - config.json
    - model.safetensors (or pytorch_model.bin)
    - tokenizer_config.json
    - vocab.txt
    - bpe.codes
    """
    print(f"🔍 Loading trained model from: {model_folder_path}")
    
    # Check if folder exists
    if not os.path.exists(model_folder_path):
        raise FileNotFoundError(f"Model folder not found: {model_folder_path}")
    
    # Check required files
    required_files = ['config.json', 'tokenizer_config.json', 'vocab.txt', 'bpe.codes']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(os.path.join(model_folder_path, file)):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️ Missing files: {missing_files}")
    
    # Check for model weights file
    model_weights_file = None
    if os.path.exists(os.path.join(model_folder_path, 'model.safetensors')):
        model_weights_file = 'model.safetensors'
    elif os.path.exists(os.path.join(model_folder_path, 'pytorch_model.bin')):
        model_weights_file = 'pytorch_model.bin'
    else:
        raise FileNotFoundError("No model weights file found (model.safetensors or pytorch_model.bin)")
    
    print(f"✅ Found model weights: {model_weights_file}")
    
    try:
        # Load model
        print("📥 Loading model...")
        model = AutoModelForSequenceClassification.from_pretrained(model_folder_path)
        
        # Load tokenizer
        print("📝 Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_folder_path)
        
        # Test the model
        print("🧪 Testing model...")
        test_text = "Congratulations! You won $10000!"
        inputs = tokenizer(test_text, return_tensors="pt", truncation=True, max_length=256, padding=True)
        
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)
            prediction = torch.argmax(probabilities, dim=-1).item()
            confidence = torch.max(probabilities).item()
        
        print(f"✅ Test prediction: {prediction} (confidence: {confidence:.3f})")
        
        # Create model data for pickle
        model_data = {
            'model': model,
            'tokenizer': tokenizer,
            'model_info': {
                'model_name': 'trained_phobert_sms_classifier',
                'num_classes': 2,
                'class_names': ['ham', 'spam'],
                'max_length': 256,
                'model_folder': model_folder_path
            }
        }
        
        return model_data
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise

def save_model_as_pickle(model_data, output_path="models/exports/phobert_sms_classifier.pkl"):
    """Save loaded model as pickle file"""
    print(f"💾 Saving model as pickle: {output_path}")
    
    # Create directory if not exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    file_size = os.path.getsize(output_path)
    print(f"✅ Model saved: {output_path} ({file_size / (1024*1024):.1f} MB)")
    
    return output_path

def test_model_predictions(model_data, test_texts=None):
    """Test model with various SMS texts"""
    if test_texts is None:
        test_texts = [
            "Congratulations! You won $10000!",
            "Hey, how are you doing?",
            "FREE MONEY!!! Click now!!!",
            "Can we meet tomorrow?",
            "Chúc mừng! Bạn đã trúng thưởng 10 triệu đồng!",
            "Xin chào, bạn có khỏe không?",
            "URGENT: Your account will be closed!",
            "Thanks for your message, see you later"
        ]
    
    print("\n🔮 Testing model predictions:")
    model = model_data['model']
    tokenizer = model_data['tokenizer']
    
    for text in test_texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256, padding=True)
        
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)
            prediction = torch.argmax(probabilities, dim=-1).item()
            confidence = torch.max(probabilities).item()
        
        prediction_text = "spam" if prediction == 1 else "ham"
        print(f"  '{text[:40]}...' -> {prediction_text} (confidence: {confidence:.3f})")

def test_with_sms_service():
    """Test model with SMS prediction service"""
    print("\n🧪 Testing with SMS prediction service...")
    
    try:
        from sms_prediction_service import SMSPredictionService
        
        # Create service instance
        service = SMSPredictionService()
        
        # Reset any previous state
        service.is_loaded = False
        service.model = None
        service.model_path = None
        
        # Try to load the model
        print("📥 Loading model through SMS service...")
        success = service.load_model()
        
        if success:
            print("✅ Model loaded successfully through SMS service!")
            
            # Test predictions
            test_messages = [
                "Congratulations! You won $10000!",
                "Hey, how are you doing?",
                "FREE MONEY!!! Click now!!!",
                "Can we meet tomorrow?"
            ]
            
            print("\n🔮 Testing predictions through SMS service:")
            for msg in test_messages:
                try:
                    result = service.predict(msg)
                    print(f"  '{msg[:30]}...' -> {result['prediction']} (confidence: {result['confidence']:.3f})")
                except Exception as e:
                    print(f"  '{msg[:30]}...' -> ERROR: {e}")
            
            return True
        else:
            print("❌ Failed to load model through SMS service")
            return False
            
    except Exception as e:
        print(f"❌ Error testing with SMS service: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Loading Trained PhoBERT SMS Classifier")
    print("=" * 60)
    
    try:
        # Load the trained model
        model_data = load_trained_model()
        
        # Test predictions
        test_model_predictions(model_data)
        
        # Save as pickle for easy loading
        pickle_path = save_model_as_pickle(model_data)
        
        # Test with SMS service
        test_with_sms_service()
        
        print("\n" + "=" * 60)
        print("✅ MODEL LOADING COMPLETE!")
        print("=" * 60)
        print(f"📁 Model folder: models/trained/")
        print(f"📁 Pickle file: {pickle_path}")
        print("\nNext steps:")
        print("1. Test the API endpoints")
        print("2. Deploy to production")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
