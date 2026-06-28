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
    
    # After field validation the code below runs
    def validate(self, attrs):
        # attrs is like a backpack containing validated details from serializers
        # below we are taking out the email and password from the backpack
        email = attrs.get("email")
        password = attrs.get("password")
        # below runs a DRF function that simply means "only verify identity"
        # expects three things; request, email, password
        school = authenticate(
            request=self.context.get("request"),
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