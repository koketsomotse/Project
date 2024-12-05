from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    
    Args:
        exc: The exception instance
        context: The context of the exception
        
    Returns:
        Response object with error details
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, there was an unhandled exception
    if response is None:
        logger.error(
            f"Unhandled exception: {str(exc)}",
            exc_info=True,
            extra={
                'view': context.get('view').__class__.__name__,
                'args': context.get('args', []),
                'kwargs': context.get('kwargs', {})
            }
        )
        
        return Response(
            {
                'error': 'An unexpected error occurred',
                'detail': str(exc) if not isinstance(exc, Exception) else exc.args[0]
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Add more context to the error response
    if isinstance(response.data, dict):
        response.data['status_code'] = response.status_code
        
        # Log the error
        logger.error(
            f"Handled exception: {str(exc)}",
            extra={
                'status_code': response.status_code,
                'view': context.get('view').__class__.__name__,
                'error_detail': response.data
            }
        )
    
    return response
