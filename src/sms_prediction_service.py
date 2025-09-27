import logging
from typing import Dict, Union
from .model_loader import get_model_loader

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SMSPredictionService:
    """
    Service để dự đoán SMS.
    Service này là một lớp vỏ mỏng (thin wrapper) quanh FraudModelLoader.
    """
    def __init__(self):
        self.model_loader = get_model_loader()

    def predict(self, sms_content: str) -> Dict[str, Union[str, float]]:
        """Dự đoán SMS bằng model đã được load."""
        if not self.model_loader.is_loaded:
            logger.warning("Model chưa được load. Trả về kết quả mặc định.")
            return {
                "prediction": "error",
                "confidence": 0.0,
                "error": "Model not loaded. Please use the /load-model endpoint first.",
                "method": "pre-check"
            }

        try:
            # Service không cần biết chi tiết model là gì, chỉ cần gọi predict
            # Dữ liệu đầu vào cần là một list
            prediction_result = self.model_loader.predict([sms_content])
            
            # Giả sử model trả về một array các kết quả
            prediction = prediction_result[0] if prediction_result else "unknown"

            # Tạm thời chưa có confidence score từ model này
            confidence = 0.9 if prediction == "spam" else 0.8 

            return {
                "prediction": prediction,
                "confidence": confidence,
                "method": "ai_model"
            }
        except Exception as e:
            logger.error(f"Lỗi khi dự đoán: {e}")
            return {
                "prediction": "error",
                "confidence": 0.0,
                "error": str(e),
                "method": "prediction_failure"
            }

    def predict_without_lazy_loading(self, sms_content: str) -> Dict[str, Union[str, float]]:
        """
        Alias cho hàm predict, vì logic lazy loading giờ đã nằm trong loader.
        Hàm này đảm bảo tính tương thích với code cũ ở main.py.
        """
        return self.predict(sms_content)
    
    # Các hàm health check và get info sẽ lấy trực tiếp từ loader
    def health_check(self) -> Dict[str, Union[str, bool]]:
        info = self.model_loader.get_model_info()
        is_healthy = self.model_loader.is_loaded
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "model_loaded": info["is_loaded"],
            "fallback_mode": False, # Không còn fallback mode trong service này
            "prediction_method": "ai_model" if is_healthy else "none"
        }
    
    def get_model_info(self) -> Dict[str, any]:
        return self.model_loader.get_model_info()

# Khởi tạo instance toàn cục của service
sms_prediction_service = SMSPredictionService()