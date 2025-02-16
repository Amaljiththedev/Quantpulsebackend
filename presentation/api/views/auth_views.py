from presentation.api.serializers.user_serializer import UserSerializer
import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, login
from infrastructure.external_services.otp_service import generate_otp, validate_otp
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

# Define a regular expression for basic email validation.
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

class EmailSubmissionsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        # Inform the user that this endpoint requires a POST
        return Response({"detail": "Submit your email via POST to receive an OTP."})
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Please provide an email address'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Validate email format using regex.
        if not re.match(EMAIL_REGEX, email):
            return Response({'error': 'Invalid email format'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if the email already exists.
        if email in get_user_model().objects.values_list('email', flat=True):
            return Response({'error': 'Email already exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Generate OTP and send it.
        otp = generate_otp(email)
        send_mail(
            subject='Your OTP for email verification',
            message=f'Your OTP is {otp}',
            from_email="noreply@example.com",
            recipient_list=[email],
        )
        # Store the submitted email in the session.
        request.session['submitted_email'] = email
        return Response({'message': 'OTP has been sent successfully.'},
                        status=status.HTTP_200_OK)


class OtpVerificationView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        return Response({"detail": "Submit the OTP via POST to verify your email."})
    
    def post(self, request, *args, **kwargs):
        # Retrieve email solely from the session.
        email = request.session.get('submitted_email')
        otp = request.data.get('otp')
        if not email or not otp:
            return Response({'error': 'OTP is required and email must be submitted via the signup endpoint.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Validate the OTP for the email from the session.
        if validate_otp(email, otp):
            # Store the validated email in the session.
            request.session['otp_validated'] = email
            return Response({'message': 'OTP validated.'},
                            status=status.HTTP_200_OK)
        return Response({'error': 'Invalid or expired OTP.'},
                        status=status.HTTP_400_BAD_REQUEST)


class PasswordCreationView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        return Response({"detail": "Submit a password via POST to create your account."})
    
    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Retrieve the validated email from the session.
        email = request.session.get('otp_validated')
        if not email:
            return Response({'error': 'OTP not validated for any email.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Create the user using the email from the session.
        serializer = UserSerializer(data={'email': email, 'password': password})
        if serializer.is_valid():
            user = serializer.save()
            # Generate tokens after the user is saved.
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            bearer_token = f"Bearer {access_token}"
            # Log the user in (this sets an HTTP-only session cookie).
            login(request, user)
            # Clear session keys.
            request.session.pop('otp_validated', None)
            request.session.pop('submitted_email', None)
            response = Response({'message': 'User created and logged in.'},
                                status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='access_token',
                value=bearer_token,
                httponly=True,   # The cookie is not accessible via JavaScript.
                secure=False,    # Set to True in production (requires HTTPS).
                samesite='Lax'   # Adjust as needed (Lax, Strict, or None).
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
