"""
Model loader utility để load model từ Hugging Face Hub
"""
import os
import pickle
import logging
from pathlib import Path
from typing import Optional, Any, Dict
import tempfile
from huggingface_hub import hf_hub_download, snapshot_download
import shutil

logger = logging.getLogger(__name__)

class FraudModelLoader:
    def __init__(
        self, 
        repo_id: str = "hoangson2006/vietnamese-fraud-detection",
        cache_dir: Optional[str] = None
    ):
        self.repo_id = repo_id
        self.cache_dir = cache_dir or os.path.join(tempfile.gettempdir(), "fraud_model_cache")
        self.model = None
        self.support_files = {}
        self.is_loaded = False
        self.download_attempts = 0
        self.max_download_attempts = 3
        
        # Main model file name in HF repository
        self.main_model_filename = "phobert_complete_with_dependencies.pkl"
        self.support_folder_name = "phobert_model_addons"
        
    def download_model_files(self) -> Dict[str, str]:
        """Download tất cả files cần thiết từ Hugging Face với error handling"""
        
        if self.download_attempts >= self.max_download_attempts:
            raise Exception(f"Đã vượt quá {self.max_download_attempts} lần thử download")
        
        self.download_attempts += 1
        
        try:
            logger.info(f"🔄 Đang download model từ {self.repo_id} (lần thử {self.download_attempts})")
            logger.info("⏳ Model size: 517MB - có thể mất 1-3 phút...")
            
            # Method 1: Download entire repository (recommended for support files)
            try:
                local_dir = snapshot_download(
                    repo_id=self.repo_id,
                    cache_dir=self.cache_dir,
                    local_files_only=False,
                    allow_patterns=["*.pkl", f"{self.support_folder_name}/**"]
                )
                logger.info(f"✅ Đã download repository về: {local_dir}")
                
                model_files = {
                    "model_path": None,
                    "local_dir": local_dir,
                    "support_dir": None
                }
                
                # Tìm file model chính
                model_path = Path(local_dir) / self.main_model_filename
                if model_path.exists():
                    model_files["model_path"] = str(model_path)
                    logger.info(f"✅ Tìm thấy model file: {model_path}")
                else:
                    logger.warning(f"⚠️ Không tìm thấy {self.main_model_filename}")
                
                # Tìm folder support
                support_dir = Path(local_dir) / self.support_folder_name
                if support_dir.exists():
                    model_files["support_dir"] = str(support_dir)
                    logger.info(f"✅ Tìm thấy support folder: {support_dir}")
                else:
                    logger.warning(f"⚠️ Không tìm thấy folder {self.support_folder_name}")
                
                return model_files
                
            except Exception as e:
                logger.warning(f"Snapshot download failed: {e}")
                logger.info("Fallback to individual file download...")
                
                # Method 2: Download individual file
                model_path = hf_hub_download(
                    repo_id=self.repo_id,
                    filename=self.main_model_filename,
                    cache_dir=self.cache_dir
                )
                logger.info(f"✅ Downloaded main model: {model_path}")
                
                return {
                    "model_path": model_path,
                    "local_dir": str(Path(model_path).parent),
                    "support_dir": None
                }
            
        except Exception as e:
            logger.error(f"❌ Download failed (attempt {self.download_attempts}): {e}")
            
            if self.download_attempts < self.max_download_attempts:
                logger.info("🔄 Sẽ thử lại sau 10 giây...")
                import time
                time.sleep(10)
                return self.download_model_files()
            else:
                raise Exception(f"Không thể download model sau {self.max_download_attempts} lần thử: {e}")
    
    def load_model(self) -> Any:
        """Load model chính với comprehensive error handling"""
        try:
            if self.model is not None and self.is_loaded:
                logger.info("✅ Model đã được load từ cache")
                return self.model
            
            logger.info("🚀 Bắt đầu load model từ Hugging Face...")
            
            # Download files
            model_files = self.download_model_files()
            
            if not model_files["model_path"] or not os.path.exists(model_files["model_path"]):
                raise FileNotFoundError("Không tìm thấy file model sau khi download")
            
            # Verify file size
            file_size = os.path.getsize(model_files["model_path"])
            expected_size = 500 * 1024 * 1024  # ~500MB
            
            if file_size < expected_size:
                raise ValueError(f"File model quá nhỏ: {file_size} bytes, expected: {expected_size}")
            
            logger.info(f"📊 Model file size: {file_size / (1024*1024):.1f} MB")
            
            # Load model với error handling
            logger.info("📥 Đang load model từ pickle...")
            try:
                with open(model_files["model_path"], 'rb') as f:
                    self.model = pickle.load(f)
                logger.info("✅ Đã load model thành công")
            except Exception as pickle_error:
                logger.error(f"❌ Lỗi load pickle: {pickle_error}")
                raise
            
            # Load support files nếu có
            if model_files.get("support_dir") and os.path.exists(model_files["support_dir"]):
                self._load_support_files(model_files["support_dir"])
            
            # Validate model
            self._validate_model()
            
            self.is_loaded = True
            self.download_attempts = 0  # Reset on success
            
            logger.info(f"🎉 Model loaded thành công từ {self.repo_id}")
            return self.model
            
        except Exception as e:
            logger.error(f"❌ Lỗi load model: {e}")
            self.is_loaded = False
            raise
    
    def _validate_model(self):
        """Validate model có các method cần thiết"""
        if self.model is None:
            raise ValueError("Model is None sau khi load")
        
        # Check for required methods
        required_methods = ['predict']
        missing_methods = []
        
        for method in required_methods:
            if not hasattr(self.model, method):
                missing_methods.append(method)
        
        if missing_methods:
            logger.warning(f"⚠️ Model thiếu methods: {missing_methods}")
            # Kiểm tra xem có phải là dict chứa model không
            if isinstance(self.model, dict):
                if 'model' in self.model:
                    logger.info("📦 Detected model wrapped in dict, extracting...")
                    actual_model = self.model['model']
                    if hasattr(actual_model, 'predict'):
                        self.model = actual_model
                        logger.info("✅ Extracted model from dict wrapper")
                    else:
                        raise ValueError("Model trong dict cũng không có method predict")
                else:
                    raise ValueError("Model dict không chứa key 'model'")
            else:
                # Thử wrap model để có predict method
                self._try_wrap_model()
    
    def _try_wrap_model(self):
        """Thử wrap model nếu không có predict method"""
        logger.info("🔧 Thử wrap model để có predict method...")
        
        if hasattr(self.model, '__call__'):
            # Tạo wrapper cho callable model
            original_model = self.model
            
            class ModelWrapper:
                def __init__(self, model):
                    self._model = model
                
                def predict(self, X):
                    return self._model(X)
                
                def __getattr__(self, name):
                    return getattr(self._model, name)
            
            self.model = ModelWrapper(original_model)
            logger.info("✅ Wrapped callable model")
        else:
            raise ValueError("Model không có predict method và không callable")
    
    def _load_support_files(self, support_dir: str):
        """Load các files hỗ trợ từ phobert_model_addons"""
        support_path = Path(support_dir)
        
        logger.info(f"📂 Loading support files từ {support_dir}")
        
        # Load tất cả .pkl files trong support folder
        for file_path in support_path.rglob("*.pkl"):
            file_name = file_path.stem
            try:
                with open(file_path, 'rb') as f:
                    self.support_files[file_name] = pickle.load(f)
                logger.info(f"✅ Loaded support file: {file_name}")
            except Exception as e:
                logger.warning(f"⚠️ Không thể load support file {file_name}: {e}")
        
        # Load other files (json, txt, etc.)
        for file_path in support_path.rglob("*"):
            if file_path.is_file() and not file_path.name.endswith('.pkl'):
                file_name = file_path.name
                try:
                    if file_path.suffix.lower() == '.json':
                        import json
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.support_files[file_name] = json.load(f)
                    elif file_path.suffix.lower() == '.txt':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.support_files[file_name] = f.read()
                    logger.info(f"✅ Loaded support file: {file_name}")
                except Exception as e:
                    logger.warning(f"⚠️ Không thể load {file_name}: {e}")
        
        logger.info(f"📊 Loaded {len(self.support_files)} support files")
    
    def get_support_file(self, name: str) -> Optional[Any]:
        """Lấy support file theo tên"""
        return self.support_files.get(name)
    
    def predict(self, data) -> Any:
        """Wrapper để predict với error handling"""
        if not self.is_loaded:
            raise RuntimeError("Model chưa được load. Gọi load_model() trước.")
        
        try:
            return self.model.predict(data)
        except Exception as e:
            logger.error(f"❌ Lỗi prediction: {e}")
            raise
    
    def predict_proba(self, data) -> Any:
        """Wrapper để predict probability"""
        if not self.is_loaded:
            raise RuntimeError("Model chưa được load. Gọi load_model() trước.")
        
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(data)
        else:
            raise AttributeError("Model không hỗ trợ predict_proba")
    
    def clear_cache(self):
        """Xóa cache model và support files"""
        self.model = None
        self.support_files.clear()
        self.is_loaded = False
        self.download_attempts = 0
        logger.info("🧹 Đã xóa model cache")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Lấy thông tin chi tiết về model"""
        info = {
            "repo_id": self.repo_id,
            "is_loaded": self.is_loaded,
            "model_type": type(self.model).__name__ if self.model else "None",
            "support_files_count": len(self.support_files),
            "support_files": list(self.support_files.keys()),
            "download_attempts": self.download_attempts,
            "main_filename": self.main_model_filename
        }
        
        # Model capabilities
        if self.model:
            info["has_predict"] = hasattr(self.model, 'predict')
            info["has_predict_proba"] = hasattr(self.model, 'predict_proba')
            info["has_transform"] = hasattr(self.model, 'transform')
            info["is_callable"] = hasattr(self.model, '__call__')
        
        return info

# Singleton instance để tái sử dụng
model_loader = None

def get_model_loader(repo_id: str = "your-username/vietnamese-fraud-detection-model") -> FraudModelLoader:
    """Factory function để lấy model loader singleton"""
    global model_loader
    
    if model_loader is None or model_loader.repo_id != repo_id:
        model_loader = FraudModelLoader(repo_id=repo_id)
    
    return model_loader

def load_fraud_model(repo_id: str = "your-username/vietnamese-fraud-detection-model") -> Any:
    """Convenience function để load model nhanh"""
    loader = get_model_loader(repo_id)
    return loader.load_model()