from django.db import models
from .custom_user import User 
from gdstorage.storage import GoogleDriveStorage 

gd_storage = GoogleDriveStorage()

# Create your models here.

class SingleChat(models.Model):
  user_1 = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="first_user")
  user_2 = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="second_user")
  created_on = models.DateTimeField(auto_now_add=True,blank=True)
  recent_msg = models.TextField(blank=True)
  class Meta:
    unique_together =["user_1","user_2"]
    
  def __str__(self):
    return f"{self.user_1.username} and {self.user_2.username}"
  

class SingleChatMessage(models.Model):
  first_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="firstchat_user")
  second_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="secchat_user")
  message = models.TextField()
  reply = models.ForeignKey("self",on_delete=models.SET_NULL,blank=True,null=True)
  timestamp = models.DateTimeField(auto_now_add=True,blank=True)
  
  def __str__(self):
    return self.message[0:50]


class Group(models.Model):
 admin = models.ForeignKey(User,on_delete=models.CASCADE)
 logo = models.ImageField(upload_to="chat/group/logo",storage=gd_storage,blank=True)
 name = models.CharField(max_length=100)
 users = models.ManyToManyField(User,related_name='group_users',blank=True)
 description = models.TextField(blank=True)
 created_on = models.DateField(auto_now_add=True,blank=True)
 recent_msg = models.TextField(blank=True)
 def __str__(self):
   return self.name 
   
class GroupMessage(models.Model):
  group = models.ForeignKey(Group,on_delete=models.CASCADE)
  user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
  reply = models.ForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True)
  message = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True,blank=True)
  
  def __str__(self):
    return self.message[0:50]

class Contact(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  contact_users = models.ManyToManyField(User,blank=True,related_name="contact_users")
  
  def __str__(self):
    return self.user.email 
    