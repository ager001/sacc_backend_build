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
        # self refers to the current manager (SchoolManager).
        # inshort it is simply BaseUserManager.create() behind the scenes
        #normalize_email() cleans the email before saving it.
        # *args This passes along any extra unnamed arguments.
        user=self.create(email=self.normalize_email(email), *args, **kwargs)
        #Django hashes (encrypts) the password before saving it.
        user.set_password(password)
        #This gives the user staff privileges.
        user.is_staff=True
        #writes the record into the database.
        user.save(using=self._db)
        #The function is finished.It returns the newly created School object.
        #That means another part of your application can immediately use it.
        return user
    

#This creates a new model called School.
#Instead of inheriting from the normal Django Model, it inherits from: AbstractBaseUser
#This model can authenticate (log in) like a user.
class School (AbstractBaseUser):
    name=models.CharField(max_length=50, null=False, blank=False)
    email=models.EmailField(unique=True, null=False)
    box=models.IntegerField(blank=False, null=False)
    address=models.IntegerField(blank=False, null=False)
    phone_number=models.CharField(blank=False, null=False, max_length=15)
    town=models.CharField(blank=False, null=False, max_length=100)
    is_active=models.BooleanField(default=True)
      
    USERNAME_FIELD = "email"
    objects=SchoolManager()
    
    def __str__(self):
        return f"School Name:{self.name} Phone:{self.phone_number}"
