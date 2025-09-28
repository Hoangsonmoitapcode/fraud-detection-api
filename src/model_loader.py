import os
import logging
import time
import torch
from typing import Dict, List, Union, Optional, Any
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
from huggingface_hub import login, HfApi
import numpy as np

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FraudModelLoader:
    """
    Vietnamese Fraud Detection Model Loader for PhoBERT
    Tối ưu cho Railway deployment với memory-efficient loading
    """
    
    def __init__(self, model_name: str = "hoangson2006/vietnamese-fraud-detection"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.config = None
        self.is_loaded = False
        self.load_attempts = 0
        self.last_load_time = None
        self.load_error = None
        
        # Cache directories
        self.cache_dir = os.getenv('TRANSFORMERS_CACHE', '/opt/venv/model_cache')
        self.hf_token = os.getenv('HF_TOKEN')
        
        # Model configuration
        self.max_length = 256  # Optimal for SMS content
        self.device = torch.device('cpu')  # Force CPU for Railway
        
        logger.info(f"🤖 Initialized FraudModelLoader for {self.model_name}")
        logger.info(f"📁 Cache directory: {self.cache_dir}")
        logger.info(f"💻 Device: {self.device}")

    def _login_to_huggingface(self) -> bool:
        """Login to Hugging Face if token is available"""
        try:
            if self.hf_token:
                login(token=self.hf_token)
                logger.info("✅ Logged in to Hugging Face")
                return True
            else:
                logger.warning("⚠️ No HF_TOKEN found - proceeding without authentication")
                return False
        except Exception as e:
            logger.warning(f"⚠️ HF login failed: {e}")
            return False

    def _check_model_exists(self) -> bool:
        """Check if model exists on Hugging Face Hub"""
        try:
            api = HfApi()
            model_info = api.model_info(self.model_name)
            logger.info(f"✅ Model found on Hub: {model_info.modelId}")
            return True
        except Exception as e:
            logger.error(f"❌ Model not found on Hub: {e}")
            return False

    def _load_model_components(self):
        """Load tokenizer, config, and model with memory optimization"""
        start_time = time.time()
        
        try:
            # Login first
            self._login_to_huggingface()
            
            # Check if model exists
            if not self._check_model_exists():
                raise Exception(f"Model {self.model_name} not found on Hugging Face Hub")
            
            logger.info("📥 Loading model components...")
            
            # Load config first (lightweight)
            logger.info("📋 Loading model config...")
            self.config = AutoConfig.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir,
                token=self.hf_token
            )
            logger.info(f"✅ Config loaded: {self.config.num_labels} labels")
            
            # Load tokenizer (lightweight)
            logger.info("🔤 Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir,
                token=self.hf_token
            )
            logger.info("✅ Tokenizer loaded successfully")
            
            # Load model (heavyweight - optimize memory)
            logger.info("🧠 Loading PhoBERT model...")
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir,
                token=self.hf_token,
                torch_dtype=torch.float32,  # Use float32 for CPU
                low_cpu_mem_usage=True,     # Memory optimization
                device_map='cpu'            # Force CPU
            )
            
            # Move to CPU and set to eval mode
            self.model.to(self.device)
            self.model.eval()
            
            # Disable gradients for inference (save memory)
            for param in self.model.parameters():
                param.requires_grad = False
                
            load_time = time.time() - start_time
            logger.info(f"✅ Model loaded successfully in {load_time:.2f}s")
            logger.info(f"📊 Model size: ~{self._estimate_model_size():.1f}MB")
            
            self.is_loaded = True
            self.last_load_time = time.time()
            self.load_error = None
            
        except Exception as e:
            load_time = time.time() - start_time
            self.load_error = str(e)
            logger.error(f"❌ Model loading failed after {load_time:.2f}s: {e}")
            raise e

    def _estimate_model_size(self) -> float:
        """Estimate model size in MB"""
        if not self.model:
            return 0.0
        
        param_size = 0
        buffer_size = 0
        
        for param in self.model.parameters():
            param_size += param.nelement() * param.element_size()
        
        for buffer in self.model.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()
        
        size_mb = (param_size + buffer_size) / 1024 / 1024
        return size_mb

    def load_model(self):
        """Load model with error handling and retry logic"""
        self.load_attempts += 1
        
        try:
            logger.info(f"🚀 Loading model attempt #{self.load_attempts}")
            self._load_model_components()
            logger.info("🎉 Model loading completed successfully!")
            
        except Exception as e:
            logger.error(f"💥 Model loading failed: {e}")
            self.is_loaded = False
            raise e

    def predict(self, texts: List[str]) -> List[str]:
        """
        Predict spam/ham for SMS texts
        Args:
            texts: List of SMS content strings
        Returns:
            List of predictions ('spam' or 'ham')
        """
        if not self.is_loaded:
            logger.error("❌ Model not loaded. Call load_model() first.")
            raise RuntimeError("Model not loaded")
        
        if not texts:
            return []
        
        try:
            logger.info(f"🔍 Predicting {len(texts)} SMS messages...")
            
            # Tokenize input texts
            inputs = self.tokenizer(
                texts,
                truncation=True,
                padding=True,
                max_length=self.max_length,
                return_tensors="pt"
            )
            
            # Move inputs to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Inference with no gradients (memory efficient)
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                predicted_classes = torch.argmax(predictions, dim=-1)
            
            # Convert to labels
            results = []
            for pred in predicted_classes.cpu().numpy():
                # Assuming: 0 = ham, 1 = spam (adjust based on your model)
                label = "spam" if pred == 1 else "ham"
                results.append(label)
            
            logger.info(f"✅ Prediction completed: {results}")
            return results
            
        except Exception as e:
            logger.error(f"❌ Prediction failed: {e}")
            raise e

    def predict_single(self, text: str) -> Dict[str, Union[str, float]]:
        """
        Predict single SMS with confidence score
        Args:
            text: SMS content string
        Returns:
            Dict with prediction and confidence
        """
        if not self.is_loaded:
            return {
                "prediction": "error",
                "confidence": 0.0,
                "error": "Model not loaded"
            }
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text,
                truncation=True,
                padding=True,
                max_length=self.max_length,
                return_tensors="pt"
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
                confidence, predicted_class = torch.max(probabilities, dim=-1)
            
            # Convert to label
            pred_class = predicted_class.item()
            confidence_score = confidence.item()
            
            # Assuming: 0 = ham, 1 = spam
            prediction = "spam" if pred_class == 1 else "ham"
            
            return {
                "prediction": prediction,
                "confidence": confidence_score,
                "class_id": pred_class
            }
            
        except Exception as e:
            logger.error(f"❌ Single prediction failed: {e}")
            return {
                "prediction": "error",
                "confidence": 0.0,
                "error": str(e)
            }

    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information"""
        return {
            "model_name": self.model_name,
            "is_loaded": self.is_loaded,
            "load_attempts": self.load_attempts,
            "last_load_time": self.last_load_time,
            "load_error": self.load_error,
            "cache_directory": self.cache_dir,
            "device": str(self.device),
            "max_length": self.max_length,
            "estimated_size_mb": self._estimate_model_size() if self.is_loaded else 0,
            "num_labels": self.config.num_labels if self.config else "unknown",
            "tokenizer_vocab_size": len(self.tokenizer) if self.tokenizer else 0,
            "memory_optimized": True,
            "torch_dtype": "float32",
            "hf_token_available": bool(self.hf_token)
        }

    def health_check(self) -> Dict[str, Union[str, bool]]:
        """Perform health check on model"""
        if not self.is_loaded:
            return {
                "status": "unhealthy",
                "reason": "Model not loaded",
                "is_loaded": False
            }
        
        try:
            # Test prediction with sample text
            test_result = self.predict_single("Test message")
            
            if test_result["prediction"] == "error":
                return {
                    "status": "unhealthy",
                    "reason": f"Prediction test failed: {test_result.get('error')}",
                    "is_loaded": True
                }
            
            return {
                "status": "healthy",
                "reason": "Model operational",
                "is_loaded": True,
                "test_prediction": test_result["prediction"],
                "test_confidence": test_result["confidence"]
            }
            
        except Exception as e:
            return {
                "status": "unhealthy", 
                "reason": f"Health check failed: {str(e)}",
                "is_loaded": True
            }

    def unload_model(self):
        """Unload model to free memory"""
        logger.info("🗑️ Unloading model to free memory...")
        
        if self.model:
            del self.model
            self.model = None
            
        if self.tokenizer:
            del self.tokenizer
            self.tokenizer = None
            
        if self.config:
            del self.config
            self.config = None
        
        # Clear PyTorch cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.is_loaded = False
        logger.info("✅ Model unloaded successfully")


# Global model loader instance
_global_model_loader: Optional[FraudModelLoader] = None

def get_model_loader() -> FraudModelLoader:
    """Get the global model loader instance (singleton pattern)"""
    global _global_model_loader
    
    if _global_model_loader is None:
        _global_model_loader = FraudModelLoader()
        logger.info("🔧 Created new global model loader instance")
    
    return _global_model_loader

def get_global_model_info() -> Dict[str, Any]:
    """Get global model information"""
    loader = get_model_loader()
    return loader.get_model_info()