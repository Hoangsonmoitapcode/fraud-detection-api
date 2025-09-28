import os
import logging
import time
import pickle
from typing import Dict, List, Union, Optional, Any
from huggingface_hub import hf_hub_download, login
import numpy as np

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FraudModelLoader:
    """
    Vietnamese Fraud Detection Model Loader for Pickle Model
    Load model từ Hugging Face Hub (.pkl file)
    """
    
    def __init__(self, model_name: str = "hoangson2006/vietnamese-fraud-detection"):
        self.model_name = model_name
        self.model = None
        self.is_loaded = False
        self.load_attempts = 0
        self.last_load_time = None
        self.load_error = None
        
        # Model file info
        self.model_filename = "phobert_complete_with_dependencies.pkl"
        self.model_path = None
        
        # HF Token
        self.hf_token = os.getenv('HF_TOKEN')
        
        logger.info(f"🤖 Initialized FraudModelLoader for {self.model_name}")
        logger.info(f"📄 Model file: {self.model_filename}")

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

    def _download_model_file(self) -> str:
        """Download model file from Hugging Face Hub"""
        try:
            logger.info(f"📥 Downloading {self.model_filename} from {self.model_name}...")
            
            # Login first
            self._login_to_huggingface()
            
            # Download model file
            model_path = hf_hub_download(
                repo_id=self.model_name,
                filename=self.model_filename,
                token=self.hf_token,
                cache_dir=os.getenv('HF_HOME', '/tmp/hf_cache')
            )
            
            logger.info(f"✅ Model downloaded to: {model_path}")
            return model_path
            
        except Exception as e:
            logger.error(f"❌ Failed to download model: {e}")
            raise e

    def _load_pickle_model(self, model_path: str):
        """Load pickle model from file"""
        try:
            logger.info(f"🔄 Loading pickle model from {model_path}...")
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            logger.info("✅ Pickle model loaded successfully")
            
            # Estimate model size
            model_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
            logger.info(f"📊 Model size: {model_size:.1f}MB")
            
        except Exception as e:
            logger.error(f"❌ Failed to load pickle model: {e}")
            raise e

    def load_model(self):
        """Load model with error handling and retry logic"""
        self.load_attempts += 1
        start_time = time.time()
        
        try:
            logger.info(f"🚀 Loading model attempt #{self.load_attempts}")
            
            # Download model file
            self.model_path = self._download_model_file()
            
            # Load pickle model
            self._load_pickle_model(self.model_path)
            
            load_time = time.time() - start_time
            logger.info(f"🎉 Model loading completed successfully in {load_time:.2f}s!")
            
            self.is_loaded = True
            self.last_load_time = time.time()
            self.load_error = None
            
        except Exception as e:
            load_time = time.time() - start_time
            self.load_error = str(e)
            logger.error(f"💥 Model loading failed after {load_time:.2f}s: {e}")
            self.is_loaded = False
            raise e

    def predict(self, texts: List[str]) -> List[str]:
        """
        Predict spam/ham for SMS texts using pickle model
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
            
            # Use the loaded pickle model for prediction
            # Model expects individual strings or array-like input
            predictions = self.model.predict(texts)
            
            # Convert predictions to string labels
            results = []
            for pred in predictions:
                # Handle different prediction formats
                if isinstance(pred, (int, np.integer)):
                    # Binary classification: 0=ham, 1=spam
                    label = "spam" if pred == 1 else "ham"
                elif isinstance(pred, str):
                    # Direct string prediction
                    label = pred.lower()
                else:
                    # Convert to string and normalize
                    label = str(pred).lower()
                    if label not in ['spam', 'ham']:
                        label = "spam" if label in ['1', 'true'] else "ham"
                
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
            # Use model for single prediction
            if hasattr(self.model, 'predict_proba'):
                # If model supports probability prediction (Scikit-learn models usually do)
                probabilities = self.model.predict_proba([text])[0]
                predicted_class = np.argmax(probabilities)
                confidence = float(np.max(probabilities))
                
                # For binary classification, class 1 is usually spam
                prediction_label = "spam" if predicted_class == 1 else "ham"
                
            else:
                # Fallback to regular prediction
                prediction = self.model.predict([text])[0]
                
                # Handle different prediction formats
                if isinstance(prediction, (int, np.integer)):
                    predicted_class = prediction
                    prediction_label = "spam" if prediction == 1 else "ham"
                elif isinstance(prediction, str):
                    prediction_label = prediction.lower()
                    predicted_class = 1 if prediction_label == "spam" else 0
                else:
                    # Convert and normalize
                    prediction_str = str(prediction).lower()
                    if prediction_str in ['1', 'true', 'spam']:
                        prediction_label = "spam"
                        predicted_class = 1
                    else:
                        prediction_label = "ham"
                        predicted_class = 0
                
                confidence = 0.85  # Default confidence when no probability available
            
            return {
                "prediction": prediction_label,
                "confidence": confidence,
                "class_id": int(predicted_class)
            }
            
        except Exception as e:
            logger.error(f"❌ Single prediction failed: {e}")
            return {
                "prediction": "error",
                "confidence": 0.0,
                "error": str(e)
            }

    def _estimate_model_size(self) -> float:
        """Estimate model size in MB"""
        if not self.model_path or not os.path.exists(self.model_path):
            return 0.0
        
        size_mb = os.path.getsize(self.model_path) / (1024 * 1024)
        return size_mb

    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information"""
        return {
            "model_name": self.model_name,
            "model_filename": self.model_filename,
            "model_type": "pickle",
            "is_loaded": self.is_loaded,
            "load_attempts": self.load_attempts,
            "last_load_time": self.last_load_time,
            "load_error": self.load_error,
            "model_path": self.model_path,
            "estimated_size_mb": self._estimate_model_size(),
            "hf_token_available": bool(self.hf_token),
            "model_object_type": str(type(self.model)) if self.model else "None"
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
        
        self.is_loaded = False
        self.model_path = None
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