from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from authentication.exceptions import (
    InvalidOTP,
    InvalidRoleCredentials,
    InvalidSchoolCredentials,
    OTPExpired,
    SchoolInactive,
)

# ============================================================================
# Exception → HTTP Response Mapping
# ============================================================================
#
# This dictionary acts as a translator between our business exceptions and the
# HTTP responses expected by API clients.
#
# Key   -> Exception class raised by the service layer.
# Value -> A tuple containing:
#          1. The message to send to the client.
#          2. The HTTP status code.
#
# Why use a mapping?
#
# Instead of writing a long chain of:
#
#     if isinstance(exc, ...)
#
# we centralize all exception definitions in one place.
#
# When a new business exception is introduced, we simply add one new entry
# here without modifying the exception handler itself.
#
EXCEPTION_RESPONSE_MAPPING = {
    # AUTHENTICATION EXCEPTIONS
    InvalidSchoolCredentials: (
        "Invalid email or password.",
        status.HTTP_401_UNAUTHORIZED,
    ),
    SchoolInactive: (
        "School account is inactive.",
        status.HTTP_401_UNAUTHORIZED,
    ),
    InvalidRoleCredentials: (
        "Role credentials are invalid.",
        status.HTTP_401_UNAUTHORIZED,
    ),
    InvalidOTP: (
        "OTP is invalid.",
        status.HTTP_401_UNAUTHORIZED,
    ),
    OTPExpired: (
        "OTP has expired.",
        status.HTTP_401_UNAUTHORIZED,
    ),
}


def custom_exception_handler(exc, context):
    """
    Centralized exception handler for the entire API.

    Responsibility:
    ----------------
    Convert Python exceptions into standardized HTTP responses.

    Workflow:
    ---------
    1. Give Django REST Framework the first opportunity to handle the exception.
    2. If DRF cannot handle it, check whether it is one of our custom
       business exceptions.
    3. If it is, translate it into our standard API response format.
    4. Otherwise, return DRF's original response.
    """

    # ------------------------------------------------------------------------
    # Step 1:
    # Let DRF attempt to handle the exception using its built-in exception
    # handler.
    #
    # Examples include:
    # - ValidationError
    # - NotAuthenticated
    # - PermissionDenied
    # - NotFound
    #
    # If DRF recognizes the exception, it returns an appropriate Response.
    # Otherwise, it returns None.
    # ------------------------------------------------------------------------
    response = exception_handler(exc, context)

    # ------------------------------------------------------------------------
    # Step 2:
    # Check whether this exception exists in our custom mapping.
    #
    # type(exc) returns the exact class of the exception.
    #
    # Example:
    #
    #     SchoolInactive()
    #
    # becomes:
    #
    #     SchoolInactive
    #
    # which is then used to look up the corresponding response definition.
    # ------------------------------------------------------------------------
    exception_response = EXCEPTION_RESPONSE_MAPPING.get(type(exc))

    # ------------------------------------------------------------------------
    # Step 3:
    # If the exception exists in our mapping, build a standardized HTTP
    # response for the frontend.
    # ------------------------------------------------------------------------
    if exception_response:
        message, status_code = exception_response

        return Response(
            {
                "detail": message,
            },
            status=status_code,
        )

    # ------------------------------------------------------------------------
    # Step 4:
    # If the exception is neither one of DRF's built-in exceptions nor one of
    # our custom business exceptions, return DRF's original response.
    #
    # Keeping this return outside the custom exception logic ensures that
    # unknown exceptions continue to be handled normally.
    # ------------------------------------------------------------------------
    return response