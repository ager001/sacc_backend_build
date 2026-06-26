from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomSchoolAuth(BaseUserManager):
    def create_user(self, email, password=None, *args, **kwargs):
        if not email:
            raise ValueError("Kindly input your email for your email is required")
