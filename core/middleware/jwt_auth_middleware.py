import jwt
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

class JWTAuthenticationMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = [
            '/api/tasks',
            '/api/auth/logout',
        ]
    
    def __call__(self, request):
        if self._requires_auth(request.path):
            auth_result = self._authenticate_jwt(request)
            if not auth_result['success']:
                return JsonResponse(
                    {
                        'success': False,
                        'errors': {'general': [auth_result['message']]}
                    },
                    status=401
                )
            request.user = auth_result['user']
        
        response = self.get_response(request)
        return response
    
    def _requires_auth(self, path):
        for protected_path in self.protected_paths:
            if path.startswith(protected_path):
                return True
        return False
    
    def _authenticate_jwt(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return {
                'success': False,
                'message': 'Authorization header is required'
            }
        
        try:
            auth_parts = auth_header.split()
            if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
                return {
                    'success': False,
                    'message': 'Invalid authorization header format'
                }
            
            token = auth_parts[1]
            
            UntypedToken(token)
            
            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            
            user_id = decoded_token.get('user_id')
            if not user_id:
                return {
                    'success': False,
                    'message': 'Invalid token payload'
                }
            
            try:
                user = User.objects.get(id=user_id)
                if not user.is_active:
                    return {
                        'success': False,
                        'message': 'User account is disabled'
                    }
                
                return {
                    'success': True,
                    'user': user
                }
                
            except User.DoesNotExist:
                return {
                    'success': False,
                    'message': 'User not found'
                }
            
        except (InvalidToken, TokenError):
            return {
                'success': False,
                'message': 'Invalid or expired token'
            }
        except jwt.ExpiredSignatureError:
            return {
                'success': False,
                'message': 'Token has expired'
            }
        except jwt.InvalidTokenError:
            return {
                'success': False,
                'message': 'Invalid token'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Authentication error: {str(e)}'
            }
