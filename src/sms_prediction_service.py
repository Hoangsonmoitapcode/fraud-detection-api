import pickle
import os
import logging
from typing import Dict, Union
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SMSPredictionService:
    """Service for SMS spam/ham prediction using PhoBERT model"""
    
    def __init__(self, model_path: str = "phobert_sms_classifier.pkl"):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        
    def load_model(self) -> bool:
        """Load the PhoBERT SMS classifier model"""
        try:
            # Check if model file exists
            if not os.path.exists(self.model_path):
                logger.error(f"Model file not found: {self.model_path}")
                return False
            
            # Verify file size first
            file_size = os.path.getsize(self.model_path)
            logger.info(f"Model file size: {file_size / (1024*1024):.1f} MB")
            
            if file_size < 100 * 1024 * 1024:  # Less than 100MB
                logger.error(f"Model file too small ({file_size} bytes), likely corrupt or incomplete")
                return False
            
            # Load the pickle model with error handling
            try:
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
            except (pickle.UnpicklingError, EOFError) as e:
                logger.error(f"Pickle file corrupt: {e}")
                logger.info("Attempting to remove corrupt file...")
                try:
                    os.remove(self.model_path)
                    logger.info("Corrupt file removed")
                except:
                    pass
                return False
                
            # Extract model components
            if isinstance(model_data, dict):
                self.model = model_data.get('model')
                self.tokenizer = model_data.get('tokenizer')
                self.vectorizer = model_data.get('vectorizer')
            else:
                # If it's just the model
                self.model = model_data
                
            # Initialize PhoBERT tokenizer if not included in pickle
            if self.tokenizer is None:
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
                    logger.info("Loaded PhoBERT tokenizer from HuggingFace")
                except Exception as e:
                    logger.warning(f"Could not load PhoBERT tokenizer: {e}")
                    
            self.is_loaded = True
            logger.info(f"Successfully loaded SMS prediction model from {self.model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess SMS text for prediction"""
        # Basic text cleaning
        text = text.strip().lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def predict(self, sms_content: str) -> Dict[str, Union[str, float]]:
        """
        Predict if SMS content is spam or ham
        
        Args:
            sms_content (str): SMS message content
            
        Returns:
            Dict containing prediction result
        """
        if not self.is_loaded:
            if not self.load_model():
                return {
                    "prediction": "unknown",
                    "confidence": 0.0,
                    "error": "Model not loaded"
                }
        
        try:
            # Preprocess the input text
            processed_text = self.preprocess_text(sms_content)
            
            # Make prediction using the loaded model
            if hasattr(self.model, 'predict'):
                # For sklearn-like models
                prediction = self.model.predict([processed_text])[0]
                
                # Get prediction probability if available
                confidence = 0.5  # Default confidence
                if hasattr(self.model, 'predict_proba'):
                    proba = self.model.predict_proba([processed_text])[0]
                    confidence = max(proba)
                    
            elif hasattr(self.model, '__call__'):
                # For transformer models or callable models
                if self.tokenizer:
                    # Tokenize input
                    inputs = self.tokenizer(processed_text, return_tensors="pt", 
                                          truncation=True, max_length=256, padding=True)
                    
                    with torch.no_grad():
                        outputs = self.model(**inputs)
                        
                    # Get prediction from logits
                    if hasattr(outputs, 'logits'):
                        logits = outputs.logits
                        probabilities = torch.softmax(logits, dim=-1)
                        prediction = torch.argmax(probabilities, dim=-1).item()
                        confidence = torch.max(probabilities).item()
                    else:
                        prediction = outputs[0] if isinstance(outputs, (list, tuple)) else outputs
                        confidence = 0.5
                else:
                    # Fallback for models without tokenizer
                    prediction = self.model([processed_text])[0]
                    confidence = 0.5
            else:
                logger.error("Model doesn't have predict method or __call__")
                return {
                    "prediction": "unknown",
                    "confidence": 0.0,
                    "error": "Invalid model type"
                }
            
            # Convert prediction to spam/ham
            if isinstance(prediction, (int, np.integer)):
                result = "spam" if prediction == 1 else "ham"
            elif isinstance(prediction, str):
                result = prediction.lower()
            else:
                result = "spam" if float(prediction) > 0.5 else "ham"
                
            return {
                "prediction": result,
                "confidence": float(confidence),
                "processed_text": processed_text
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return {
                "prediction": "unknown",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Union[str, bool]]:
        """Get information about the loaded model"""
        return {
            "model_path": self.model_path,
            "is_loaded": self.is_loaded,
            "model_type": type(self.model).__name__ if self.model else "None",
            "has_tokenizer": self.tokenizer is not None
        }

# Global instance
sms_prediction_service = SMSPredictionService()
