from django.urls import path
from .views.auth_view import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('api/auth/register', RegisterView.as_view(), name='auth-register'),
    path('api/auth/login', LoginView.as_view(), name='auth-login'),
    path('api/auth/logout', LogoutView.as_view(), name='auth-logout'),
]
