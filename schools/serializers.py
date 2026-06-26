from rest_framework import serializers
from .models import School


# "Automatically create serializer fields from the School model."
class SchoolRegistrationSerializer(serializers.ModelSerializer):

    # Password should only be accepted when creating a school.
    # It should never be returned in API responses.
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        # Tell DRF which model this serializer uses.
        model = School

        # Fields accepted during registration.
        fields = [
            "id",
            "name",
            "email",
            "box",
            "address",
            "phone_number",
            "town",
            "password",
        ]
        
    # Validate
    def validate_email(self, value):
        if School.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )
        return value

    # Called after validation succeeds.
    def create(self, validated_data):

        # Remove password from the dictionary.
        password = validated_data.pop("password")

        # Use the custom manager to create the school.
        # This hashes the password automatically.
        school = School.objects.create_user(
            password=password,
            **validated_data
        )

        return school
    
    
# "Automatically create serializer fields from the School model."    
class SchoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model=School
        fields="__all__"