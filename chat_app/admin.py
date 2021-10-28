from django.contrib import admin
from  .models import * 
# Register your models here.

@admin.register(SingleChat)
class SingleChatAdmin(admin.ModelAdmin):
  list_display =["id","user_1","user_2"]
  
@admin.register(Group)
class ChatGroupAdmin(admin.ModelAdmin):
  list_display =["id","name"]
  
@admin.register(SingleChatMessage)
class ChatMessages(admin.ModelAdmin):
  list_display = ["first_user","second_user","message","reply"]
  
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display =["username","email","is_active","bio"]

@admin.register(GroupMessage)
class GroupMsgAdmin(admin.ModelAdmin):
  list_display = ["id","group","user","message"]
  
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
  list_display = ["id","user"]