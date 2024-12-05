import logging
import time
import json
from django.conf import settings

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Middleware to log all requests and responses."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Start timer
        start_time = time.time()
        
        # Log request
        self._log_request(request)
        
        # Get response
        response = self.get_response(request)
        
        # Calculate request duration
        duration = time.time() - start_time
        
        # Log response
        self._log_response(response, duration)
        
        return response
    
    def _log_request(self, request):
        """Log details of an incoming request."""
        user = request.user if hasattr(request, 'user') else 'Anonymous'
        
        # Get request body for non-GET requests
        body = None
        if request.method != 'GET':
            try:
                body = json.loads(request.body) if request.body else None
            except json.JSONDecodeError:
                body = '<Invalid JSON>'
                
        log_data = {
            'user': str(user),
            'method': request.method,
            'path': request.path,
            'query_params': dict(request.GET.items()),
            'body': body,
            'headers': dict(request.headers.items())
        }
        
        # Remove sensitive information
        if 'password' in log_data.get('body', {}):
            log_data['body']['password'] = '<redacted>'
        if 'Authorization' in log_data.get('headers', {}):
            log_data['headers']['Authorization'] = '<redacted>'
            
        logger.info(f"Request: {json.dumps(log_data)}")
    
    def _log_response(self, response, duration):
        """Log details of the response."""
        # Try to get response content
        content = None
        try:
            content = json.loads(response.content)
        except (json.JSONDecodeError, AttributeError):
            content = '<Binary or invalid JSON content>'
            
        log_data = {
            'status_code': response.status_code,
            'content': content,
            'duration': f"{duration:.2f}s",
            'headers': dict(response.headers.items())
        }
        
        logger.info(f"Response: {json.dumps(log_data)}")
