from django.contrib.auth import authenticate
from rest_framework import serializers

from schools.models import School


# This class validates credentials before creation of JWT tokens
# this is a different serializer since it doesn't create or update database
# The sole function of this serializer os to validate login details
class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    # write_only=True simply means when we return the data DRF should automatically hide the password
    # trim_whitespace=False simply means we simply tell DRF to not modify the password and authenticate with the characters supplied
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    
    # After field validation the code below runs
    def validate(self, attrs):
        # attrs is like a backpack containing validated details from serializers
        # below we are taking out the email and password from the backpack
        email = attrs.get("email")
        password = attrs.get("password")
        # the request receives the current HTTP request that the view passed into the serializer via context
        request = self.context.get("request")
        # below runs a DRF function that simply means "only verify identity"
        # expects three things; request, email, password
        school = authenticate(
            request=request,
            email=email,
            password=password
        )
        # below is a code for safety measures if authentication fails 
        # we are checking against "None" not "False"
        # because the inbuilt authenticate() should always return either User object or None
        if school is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )
        # another important line here, 
        # instead of making our views.py authenticate again, this line places our authenticated object into our back pac
        # so in simple terms only our views.py can import and retrieve it
        attrs["school"] = school

        return attrs
    
# This is the logout serializer code
class LogoutSerializer(serializers.Serializer):
    # logout serializer only has one field which is written below
    # below receives the refresh token from frontend and validates if it exists
    refresh = serializers.CharField()
    
    
    


class CurrentSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            "id",
            "name",
            "email",
        ]