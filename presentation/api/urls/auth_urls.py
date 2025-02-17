# presentation/api/urls/auth_urls.py

from django.urls import path
from presentation.api.views.auth_views import EmailSubmissionsView, OtpVerificationView, PasswordCreationView, UserLoginView, UserLogoutView

urlpatterns = [
    path('signup/', EmailSubmissionsView.as_view(), name='submit-email'),
    path('otp/', OtpVerificationView.as_view(), name='submit-otp'),
    path('password/', PasswordCreationView.as_view(), name='create-password'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
