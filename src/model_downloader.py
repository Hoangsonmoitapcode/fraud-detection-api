#!/usr/bin/env python3
"""
Model downloader service - downloads large models from cloud storage
This allows us to keep Docker image small while still having fast model access
"""

import os
import requests
import pickle
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelDownloader:
    """Downloads and caches large ML models from cloud storage"""
    
    def __init__(self, cache_dir: str = "/tmp/models"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def download_model(self, model_name: str, url: str, force_download: bool = False) -> Optional[str]:
        """
        Download model from URL and cache locally
        
        Args:
            model_name: Name of the model file
            url: URL to download from
            force_download: Force re-download even if cached
            
        Returns:
            Path to downloaded model file or None if failed
        """
        model_path = self.cache_dir / model_name
        
        # Check if already cached
        if model_path.exists() and not force_download:
            logger.info(f"Model {model_name} already cached at {model_path}")
            return str(model_path)
            
        logger.info(f"Downloading model {model_name} from {url}")
        
        try:
            # Download with progress
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(model_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Progress logging every 50MB
                        if downloaded % (50 * 1024 * 1024) == 0:
                            progress = (downloaded / total_size) * 100 if total_size else 0
                            logger.info(f"Downloaded {downloaded / (1024*1024):.1f}MB ({progress:.1f}%)")
            
            logger.info(f"Model {model_name} downloaded successfully to {model_path}")
            return str(model_path)
            
        except Exception as e:
            logger.error(f"Failed to download model {model_name}: {e}")
            # Clean up partial download
            if model_path.exists():
                model_path.unlink()
            return None
    
    def get_phobert_sms_model(self) -> Optional[str]:
        """
        Get PhoBERT SMS classifier model
        Try multiple sources in order of preference
        """
        model_name = "phobert_sms_classifier.pkl"
        
        # Try local file first (for development)
        local_path = Path("phobert_sms_classifier.pkl")
        if local_path.exists():
            logger.info(f"Using local model: {local_path}")
            return str(local_path)
        
        # Try cloud sources
        sources = [
            # You can add your cloud storage URLs here
            # "https://your-cloud-storage.com/models/phobert_sms_classifier.pkl",
            # "https://github.com/your-repo/releases/download/v1.0/phobert_sms_classifier.pkl",
        ]
        
        for url in sources:
            logger.info(f"Trying to download from: {url}")
            result = self.download_model(model_name, url)
            if result:
                return result
        
        logger.warning("Could not download PhoBERT SMS model from any source")
        return None

# Global instance
model_downloader = ModelDownloader()
