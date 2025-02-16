# presentation/api/serializers/user_serializer.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Ensure the password is write-only so it's not returned in responses.
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        # Include any fields you need; typically, you'll want id, email, etc.
        fields = ['id', 'email', 'password']
    
    def create(self, validated_data):
        """
        Create and return a new user instance, with the password properly hashed.
        """
        # Use the create_user method provided by your custom user manager.
        return User.objects.create_user(**validated_data)
