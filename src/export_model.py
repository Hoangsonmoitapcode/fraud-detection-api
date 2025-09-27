"""
Export model utilities for loading trained models
This module provides the necessary functions to load custom trained models
"""

import pickle
import torch
import numpy as np
from typing import Any, Dict, Optional
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

class ModelWrapper:
    """Wrapper class for loaded models"""
    
    def __init__(self, model):
        self.model = model
        self._setup_methods()
    
    def _setup_methods(self):
        """Setup prediction methods based on model type"""
        if hasattr(self.model, 'predict'):
            self.predict = self.model.predict
        elif hasattr(self.model, 'forward'):
            self.predict = self._torch_predict
        else:
            self.predict = self._generic_predict
    
    def _torch_predict(self, X):
        """Torch model prediction"""
        with torch.no_grad():
            if isinstance(X, (list, tuple)):
                X = torch.tensor(X)
            return self.model(X).cpu().numpy()
    
    def _generic_predict(self, X):
        """Generic prediction fallback"""
        if hasattr(self.model, '__call__'):
            return self.model(X)
        else:
            return [0] * len(X) if hasattr(X, '__len__') else [0]

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

# Create a mock module for compatibility
class MockModule:
    """Mock module for compatibility with existing pickle files"""
    
    def __init__(self):
        self.load_model_from_pickle = load_model_from_pickle
        self.save_model_to_pickle = save_model_to_pickle
        self.get_model_info = get_model_info
        self.ModelWrapper = ModelWrapper

# Create the module
export_model = MockModule()

# Make it available globally
sys.modules['export_model'] = export_model