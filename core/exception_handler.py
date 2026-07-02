from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from authentication.exceptions import (
    InvalidSchoolCredentials,
    SchoolInactive,
    InvalidRoleCredentials,
    InvalidOTP,
    OTPExpired,
)

# custom function to handle exceptions and return appropriate responses
# exc,context are the parameters that are passed to the function when an exception occurs
def custom_exception_handler(exc, context):
    # we first call the default exception handler to get the standard error response from DRF
    # if the exception is one of our custom exceptions, we return a custom response with a specific error message and status code
    response = exception_handler(exc,context)
    
    # below shows that if the response doesn't match any of DRF's default exceptions, 
    # we check if it matches any of our custom exceptions and return a custom response accordingly
    # isinstance() is a built-in Python function that checks if an object is an instance of a specified class or a subclass thereof.
    # it runs from the top of the function to the bottom, checking each exception in order. If it finds a match, it returns the corresponding response and exits the function. 
    # If it doesn't find a match, it continues to the next exception until it reaches the end of the function.
    if isinstance(exc, InvalidSchoolCredentials):
        return Response(
            {
                "detail": "Invalid email or password."
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if isinstance(exc, SchoolInactive):
        return Response(
            {
                "detail": "School account is inactive."
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if isinstance(exc, InvalidRoleCredentials):
        return Response(
            {
                "detail": "Role credentials are invalid."
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if isinstance(exc, InvalidOTP):
        return Response(
            {
                "detail": "OTP is invalid."
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if isinstance(exc, OTPExpired):
        return Response(
            {
                "detail": "OTP has expired."
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
        
    # should be outside the if statements to ensure that it is returned for all exceptions, 
    # not just the custom ones.
    return response