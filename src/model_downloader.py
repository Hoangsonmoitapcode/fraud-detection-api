"""
Model downloader for HuggingFace Hub
Downloads the PhoBERT SMS classifier model from HuggingFace Hub
"""

import os
import requests
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelDownloader:
    """Downloads model from HuggingFace Hub"""
    
    def __init__(self, model_url: str = None, local_path: str = None):
        self.model_url = model_url or "https://huggingface.co/hoangson2006/phobert-sms-classifier/resolve/main/phobert_sms_classifier.pkl"
        
        # Determine the correct path based on environment
        if os.path.exists("/app"):  # Railway production
            self.local_path = "/app/phobert_sms_classifier.pkl"
        else:  # Local development
            self.local_path = "phobert_sms_classifier.pkl"
            
        self.download_path = Path(self.local_path)
    
    def is_model_downloaded(self) -> bool:
        """Check if model is already downloaded"""
        if not self.download_path.exists():
            return False
        
        # Check if file is complete (at least 100MB)
        file_size = self.download_path.stat().st_size
        return file_size >= 100 * 1024 * 1024  # 100MB minimum
    
    def download_model(self, force_download: bool = False) -> bool:
        """
        Download model from HuggingFace Hub
        
        Args:
            force_download: Force download even if file exists
            
        Returns:
            bool: True if download successful, False otherwise
        """
        if not force_download and self.is_model_downloaded():
            logger.info(f"✅ Model already downloaded: {self.download_path}")
            return True
        
        try:
            logger.info(f"🔄 Downloading model from: {self.model_url}")
            logger.info("⏳ This may take 1-2 minutes for 518MB model...")
            
            # Create directory if not exists
            self.download_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download with progress
            response = requests.get(self.model_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(self.download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Log progress every 10MB
                        if downloaded_size % (10 * 1024 * 1024) == 0:
                            progress = (downloaded_size / total_size * 100) if total_size > 0 else 0
                            logger.info(f"📥 Downloaded: {downloaded_size / (1024*1024):.1f}MB ({progress:.1f}%)")
            
            # Verify download
            if self.is_model_downloaded():
                logger.info(f"✅ Model downloaded successfully: {self.download_path}")
                logger.info(f"📊 File size: {self.download_path.stat().st_size / (1024*1024):.1f}MB")
                return True
            else:
                logger.error("❌ Downloaded file is too small, download may have failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Download failed: {str(e)}")
            return False
    
    def get_model_path(self) -> str:
        """Get the local path to the downloaded model"""
        return str(self.download_path) if self.is_model_downloaded() else None

# Global instance
model_downloader = ModelDownloader()