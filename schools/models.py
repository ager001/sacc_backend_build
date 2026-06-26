from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# A manager talks to the database.
# It is responsible for creating users and superusers.
class SchoolManager(BaseUserManager):

    # Creates a normal school user
    def create_user(self, email, password=None, *args, **kwargs):
        if not email:
            raise ValueError("Kindly input your email because it is required.")

        # Create the model instance
        user = self.model(
            email=self.normalize_email(email),
            *args,
            **kwargs
        )

        # Hash the password
        user.set_password(password)

        # Save to the database
        user.save(using=self._db)

        return user

    # Creates an administrator
    def create_superuser(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Superusers must have an email address.")

        # Required admin permissions
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # Safety checks
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )


# Custom authentication model
class School(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=50)

    email = models.EmailField(
        unique=True
    )

    box = models.IntegerField()

    address = models.IntegerField()
        

    phone_number = models.CharField(
        max_length=15
    )

    town = models.CharField(
        max_length=100
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    # The field used for authentication
    USERNAME_FIELD = "email"

    # Fields required when creating a superuser
    REQUIRED_FIELDS = [
        "name",
        "box",
        "address",
        "phone_number",
        "town",
    ]

    # Attach the custom manager
    objects = SchoolManager()

    def __str__(self):
        return f"{self.name} ({self.email})"