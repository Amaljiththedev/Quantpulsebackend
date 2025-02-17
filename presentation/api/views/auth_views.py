import re
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from infrastructure.external_services.otp_service import generate_otp, validate_otp
from presentation.api.serializers.user_serializer import UserLoginSerializer, UserSerializer

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
            return Response({'error': 'Please provide an email address'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email format using regex.
        if not re.match(EMAIL_REGEX, email):
            return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the email already exists.
        if get_user_model().objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({'message': 'OTP has been sent successfully.'}, status=status.HTTP_200_OK)


class OtpVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')  # Get email from request body
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({'error': 'Email and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if validate_otp(email, otp):
            request.session['otp_validated'] = email
            return Response({'message': 'OTP validated.'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordCreationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')  # Fetch email from request body
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if the email exists in session (ensures OTP validation occurred)


        # Create user
        serializer = UserSerializer(data={'email': email, 'password': password})
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Log the user in
            login(request, user)

            # Clear session data
            request.session.pop('otp_validated', None)

            # Create response with JWT token as HTTP-only cookie
            response = Response({'message': 'User created and logged in.'}, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='access_token',
                value=f"Bearer {access_token}",
                httponly=True,  
                secure=False,   
                samesite='Lax'  
            )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Enter your registered email and password."})

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = get_user_model().objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        bearer_token = f"Bearer {access_token}"

        login(request, user)

        response = Response({'message': 'User logged in.'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=bearer_token,
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        return response


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Log the user out (this clears the HTTP-only session cookie).
        response = Response({'message': 'User logged out.'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        return response
