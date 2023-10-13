from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('email', 'name')

class CustomRegisterSerializer(RegisterSerializer):
    # Remove 'username' field and use 'email' field for registration
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        """
        Check if the provided email address is already registered.
        """
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email address is already registered.")
        return email

    def get_cleaned_data(self):
        """
        Get cleaned data for registration.
        """
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
        }