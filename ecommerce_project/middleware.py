from django.utils.deprecation import MiddlewareMixin
import logging  # لإضافة سجل للطلبات

logger = logging.getLogger(__name__)  # إعداد السجل

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """تسجل جميع الطلبات الواردة إلى الموقع"""
        logger.info(f"طلب جديد: {request.method} {request.path}")

    def process_response(self, request, response):
        """تسجل جميع الاستجابات التي يرسلها الموقع"""
        logger.info(f"استجابة: {response.status_code} {request.path}")
        return response