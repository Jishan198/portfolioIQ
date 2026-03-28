from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        # Use create_user to ensure the password gets hashed properly
        user = User.objects.create_user(
            username=validated_data['email'], # Django requires username, so we mirror the email
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user