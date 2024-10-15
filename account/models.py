from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, tc, phoneNumber,password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
          phoneNumber=phoneNumber,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          phoneNumber="909090909090",
          tc=tc,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.CharField(max_length=150,null=False,blank=False ,default=date.today)
  phoneNumber=models.CharField(max_length=2322,null=False,default=False)
  updated_at = models.DateTimeField(auto_now=True)
  auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']

  def __str__(self):
      return self.email

  def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }   

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin


#Phone Number OTP Model
class PhoneOTP(models.Model):
 
    phone_regex = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 14 digits allowed.")
    phone       = models.CharField(validators =[phone_regex], max_length=17, unique = True)
    otp         = models.CharField(max_length=9, blank = True, null=True)
    count       = models.IntegerField(default=0, help_text = 'Number of otp_sent')
    validated   = models.BooleanField(default = False, help_text = 'If it is true, that means user have validate otp correctly in second API')
    otp_session_id = models.CharField(max_length=120, null=True, default = "")
    username    = models.CharField(max_length=20, blank = True, null = True, default = None )
    email       = models.CharField(max_length=50, null = True, blank = True, default = None) 
    password    = models.CharField(max_length=100, null = True, blank = True, default = None) 

    

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)   
import datetime
class ReviewSection(models.Model):
    title= models.CharField(max_length=2322, blank = True, null=True)
    description= models.CharField(max_length=2322, blank = True, null=True)
    profile= models.CharField(max_length=2322, blank = True, null=True)
    role= models.CharField(max_length=2322, blank = True, null=True)
    rating= models.CharField(max_length=2322, blank = True, null=True)
    image =models.CharField(max_length=23222222222222,blank=True ,null=True)
    created_at=models.CharField(max_length=150,null=False,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))


class TelemetryDaa(models.Model):
    data= models.CharField(max_length=121111, blank = True, null=True)
    teleId= models.IntegerField(null=True,default=None)
    date = models.CharField(max_length=10,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))
    def __str__(self):
        return str(self.teleId) 

class JobApply(models.Model):
    name= models.CharField(max_length=200)
    phone = models.CharField(max_length=17,blank=True)
    email = models.CharField(max_length=50, null = True, blank = True)
    title = models.CharField(max_length=20,null = True,blank=True)
    Introduction = models.CharField(max_length=2000, null=True,blank=True)
    filename =models.FileField(max_length=232222,blank=True ,null=True)
    created_at = models.CharField(max_length=150,null=False,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))
class JobsRequired(models.Model):
    profile = models.CharField(max_length=200)
    no_of_openings = models.IntegerField(null=True,default=None)
    title = models.CharField(max_length=2322, blank = True, null=True)
    description = models.CharField(max_length=2000, null=True)
    job_responsiblity = models.CharField(max_length=200)
    technical_skills = models.CharField(max_length=200)
    Preferred_qualification = models.CharField(max_length=200,null=True)
    education = models.CharField(max_length=200,null=True)
    created_at = models.CharField(max_length=150,null=False,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))
