#!/usr/bin/env python3
"""
Pre-cache ML models during Docker build to reduce startup time
"""

import os
import sys

def cache_models():
    """Pre-download and cache ML models"""
    print("🔄 Starting model caching...")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} loaded")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import transformers
        print(f"✅ Transformers {transformers.__version__} loaded")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    # Cache PhoBERT model
    try:
        from transformers import AutoTokenizer, AutoModel
        
        print("📥 Downloading PhoBERT tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base')
        print("✅ PhoBERT tokenizer cached")
        
        print("📥 Downloading PhoBERT model...")
        model = AutoModel.from_pretrained('vinai/phobert-base')
        print("✅ PhoBERT model cached")
        
        # Test the model briefly
        print("🧪 Testing model...")
        inputs = tokenizer("Xin chào", return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        print("✅ Model test successful")
        
        return True
        
    except Exception as e:
        print(f"⚠️ PhoBERT caching failed: {e}")
        print("📝 Model will be downloaded at runtime")
        return False

if __name__ == "__main__":
    success = cache_models()
    print(f"🏁 Model caching {'completed' if success else 'finished with warnings'}")
    # Don't exit with error even if caching fails
    sys.exit(0)
