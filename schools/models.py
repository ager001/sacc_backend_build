from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# A manager talks to the database, they answer CRUD operations questions
# SchoolManager inherits everything from BaseUserManager
# Now SchoolManager already knows many authentication-related operations.
# We only need to customize what we want
class SchoolManager(BaseUserManager):
    # Below we have defined how a normal user should be created 
    # Required pieces of information is; email(instead of username), password=None simply stores password safely
    # args=Accept extra unnamed arguments kwargs=Accept extra named arguments.
    def create_user(self, email, password=None, *args, **kwargs):
        #if no email provided, raise ValueError, if yes execute next line
        if not email:
            raise ValueError("Kindly input your email for your email is required")
