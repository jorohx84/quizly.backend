from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Adds a 'confirmed_password' field to verify that the user entered
    the password correctly twice.

    Methods:
        validate(attrs):
            Checks that 'password' and 'confirmed_password' match.
            Raises a ValidationError if they do not.

        create(validated_data):
            Removes 'confirmed_password' from validated data and
            creates a new User instance using the remaining data.
    """
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError({"password": "password do not match"})
        return attrs
    

    def create(self, validated_data):
        validated_data.pop('confirmed_password')
        user = User.objects.create_user(**validated_data)
        return user
    