"""
Export model utilities for loading trained models
This module provides the necessary functions to load custom trained models
"""

import pickle
import torch
import numpy as np
from typing import Any, Dict, Optional
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

class PhoBERTSMSClassifier(nn.Module):
    """PhoBERT SMS Classifier model"""
    
    def __init__(self, num_classes=2, model_name="vinai/phobert-base-v2"):
        super(PhoBERTSMSClassifier, self).__init__()
        self.num_classes = num_classes
        self.model_name = model_name
        
        # Load PhoBERT model
        self.phobert = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.phobert.config.hidden_size, num_classes)
        
    def forward(self, input_ids, attention_mask=None):
        """Forward pass"""
        outputs = self.phobert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        return self.classifier(pooled_output)
    
    def predict(self, input_ids, attention_mask=None):
        """Prediction method"""
        with torch.no_grad():
            outputs = self.forward(input_ids, attention_mask)
            predictions = torch.softmax(outputs, dim=-1)
            return torch.argmax(predictions, dim=-1)
    
    def predict_proba(self, input_ids, attention_mask=None):
        """Prediction probabilities"""
        with torch.no_grad():
            outputs = self.forward(input_ids, attention_mask)
            return torch.softmax(outputs, dim=-1)

def load_model_from_pickle(file_path: str) -> Any:
    """
    Load a model from pickle file with proper error handling
    
    Args:
        file_path: Path to the pickle file
        
    Returns:
        Loaded model object
    """
    try:
        with open(file_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        raise Exception(f"Failed to load model from {file_path}: {str(e)}")

def save_model_to_pickle(model: Any, file_path: str) -> None:
    """
    Save a model to pickle file
    
    Args:
        model: Model object to save
        file_path: Path to save the model
    """
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(model, f)
    except Exception as e:
        raise Exception(f"Failed to save model to {file_path}: {str(e)}")

def get_model_info(model: Any) -> Dict[str, Any]:
    """
    Get information about a loaded model
    
    Args:
        model: Loaded model object
        
    Returns:
        Dictionary with model information
    """
    info = {
        "model_type": type(model).__name__,
        "has_predict": hasattr(model, 'predict'),
        "has_predict_proba": hasattr(model, 'predict_proba'),
        "has_forward": hasattr(model, 'forward'),
        "is_torch_model": isinstance(model, torch.nn.Module),
        "is_sklearn_model": hasattr(model, 'fit') and hasattr(model, 'predict')
    }
    
    # Add more specific info based on model type
    if hasattr(model, 'n_features_in_'):
        info["n_features"] = model.n_features_in_
    if hasattr(model, 'classes_'):
        info["classes"] = model.classes_.tolist() if hasattr(model.classes_, 'tolist') else list(model.classes_)
    if hasattr(model, 'n_classes_'):
        info["n_classes"] = model.n_classes_
        
    return info