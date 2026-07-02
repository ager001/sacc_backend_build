class AuthenticationError(Exception):
    """Base class for all authentication errors."""
    pass


class InvalidSchoolCredentials(AuthenticationError):
    """School email or password is incorrect."""
    pass


class SchoolInactive(AuthenticationError):
    """School account is inactive."""
    pass


class InvalidRoleCredentials(AuthenticationError):
    """Role credentials are invalid."""
    pass


class InvalidOTP(AuthenticationError):
    """OTP is invalid."""
    pass


class OTPExpired(AuthenticationError):
    """OTP has expired."""
    pass