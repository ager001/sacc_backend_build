from django.contrib.auth import authenticate
from rest_framework import serializers


# This class validates credentials before creation of JWT tokens
# this is a different serializer since it doesn't create or update database
# The sole function of this serializer os to validate login details
class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )