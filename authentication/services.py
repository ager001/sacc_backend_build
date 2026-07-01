from schools.models import School
from django.core.exceptions import ValidationError

# the class below is a service class that handles the business logic for authentication
class AuthenticationService:
    # the method below verifies the school credentials
    def verify_school(self, validated_data):
        # extract the email and password from the validated data
        email = validated_data["email"]
        password = validated_data["password"]
        
        # if the school matches the email and password, return the school object
        try:
            school = School.objects.get(email=email)
        # if the school does not exist, raise a validation error
        except School.DoesNotExist:
            raise ValidationError(
                "Invalid email or password."
            )
        # if the password does not match raise a validation error
        if not school.check_password(password):
            raise ValidationError(
                "Invalid email or password."
            )
        # if the school is not active raise the same validation error to avoid account enumeration
        if not school.is_active:
            raise ValidationError(
                "Invalid email or password."
            )
        # finally return the school object if all checks pass
        return school

# the line of code below creates an instance of the AuthenticationService class that can be used in other parts of the application
authentication_service = AuthenticationService()