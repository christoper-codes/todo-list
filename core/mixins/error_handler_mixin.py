from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.http import Http404
import logging


class ErrorHandlerMixin:
    
    def validate_serializer(self, serializer):
        """Helper global para validar serializer y lanzar error automáticamente"""
        if not serializer.is_valid():
            from rest_framework.exceptions import ValidationError as DRFValidationError
            raise DRFValidationError({'errors': serializer.errors})
        return serializer.validated_data
    
    def validate_request(self, serializer_class, data, partial=False):
        serializer = serializer_class(data=data, partial=partial)
        
        if not serializer.is_valid():
            return self.validation_error_response(
                errors=serializer.errors,
                message="Invalid input data"
            )
        
        return serializer.validated_data
    
    def validate_id_param(self, param_value, param_name="ID"):
        if not param_value:
            return Response({
                'message': f'{param_name} parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not param_value.isdigit():
            return Response({
                'message': f'{param_name} must be a valid positive number'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if int(param_value) <= 0:
            return Response({
                'message': f'{param_name} must be greater than 0'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return None
    
    def handle_error(self, exception, default_message="An error occurred"):
        from rest_framework.exceptions import ValidationError as DRFValidationError
        
        if isinstance(exception, DRFValidationError):
            return Response(exception.detail, status=status.HTTP_400_BAD_REQUEST)
        
        elif isinstance(exception, ValidationError):
            return Response({
                'errors': {'validation': [str(exception)]}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif isinstance(exception, Http404):
            return Response({
                'errors': {'general': ['Resource not found']}
            }, status=status.HTTP_404_NOT_FOUND)
        
        else:
            logger = logging.getLogger(__name__)
            logger.error(f"Error in {self.__class__.__name__}: {str(exception)}", exc_info=True)
            
            return Response({
                'errors': {'general': [default_message]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def success_response(self, data=None, message="Operation successful", status_code=status.HTTP_200_OK):
        response_data = {
            'message': message
        }
        
        if data is not None:
            response_data['data'] = data
            
        return Response(response_data, status=status_code)
    
    def validation_error_response(self, errors, message="Invalid input data"):
        return Response({
            'message': message,
            'errors': errors,
            'error_type': 'validation_error'
        }, status=status.HTTP_400_BAD_REQUEST)
