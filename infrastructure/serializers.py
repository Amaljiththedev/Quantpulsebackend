from rest_framework import serializers
from infrastructure.database.user_models import CustomUser  # Importing correctly

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  # Or specify fields like ['id', 'email', 'name']
