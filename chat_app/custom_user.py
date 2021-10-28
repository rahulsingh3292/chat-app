from django.contrib.auth.base_user import BaseUserManager 
from django.contrib.auth.models import AbstractUser 
from django.db import models
from gdstorage.storage import GoogleDriveStorage

gd_storage = GoogleDriveStorage()
 
class UserManager(BaseUserManager):
  use_in_migrations = True 
  
  def create_user(self,username,email,password=None,**extra_fileds):
    if not email:
      raise ValueError("Email is required")
    if not username:
      raise ValueError("Username Missing")
    extra_fileds.setdefault("is_superuser",False)
    extra_fileds.setdefault("is_staff",False)
    email = self.normalize_email(email)
    user = self.model(username=username,email=email,password=password,**extra_fileds)
    user.set_password(password)
    user.save(using=self._db)
    return user 
  
  def create_superuser(self,username,email,password=None,**extra_fileds):
    if not email:
      raise ValueError("Email is required")
    extra_fileds.setdefault("is_staff",True)
    extra_fileds.setdefault("is_superuser",True)
    return self.create_user(username,email,password,**extra_fileds)

class User(AbstractUser):
  username = models.CharField(max_length=20)
  email = models.EmailField(max_length=150,unique=True)
  photo = models.ImageField(upload_to="chat/Images",storage=gd_storage,blank=True)
  bio = models.CharField(max_length=60,blank=True)
  last_seen = models.DateTimeField(auto_now_add=True,blank=True,null=True)
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS =["username"]
  objects = UserManager()
  
  def __str__(self):
    return str(self.email)
    
  
  