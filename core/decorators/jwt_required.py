from functools import wraps
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

def jwt_required(view_func):
    """
    Decorador que requiere autenticación JWT
    """
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        jwt_auth = JWTAuthentication()
        
        try:
            auth_result = jwt_auth.authenticate(request)
            
            if auth_result is None:
                return JsonResponse(
                    {
                        'success': False,
                        'errors': {'general': ['Authentication credentials were not provided']}
                    },
                    status=401
                )
            
            user, token = auth_result
            request.user = user
            request.auth = token
            
            return view_func(self, request, *args, **kwargs)
            
        except InvalidToken:
            return JsonResponse(
                {
                    'success': False,
                    'errors': {'general': ['Invalid or expired token']}
                },
                status=401
            )
        except Exception as e:
            return JsonResponse(
                {
                    'success': False,
                    'errors': {'general': [f'Authentication error: {str(e)}']}
                },
                status=401
            )
    
    return wrapper
