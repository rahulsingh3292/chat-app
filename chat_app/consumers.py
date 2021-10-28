from channels.generic.websocket import AsyncWebsocketConsumer
import json 
from django.utils import timezone
from channels.db import database_sync_to_async
from .helpers import create_conversation
from  .models import (User,SingleChatMessage,Group,GroupMessage ,SingleChat )
from django.db.models import Q 

SCM = SingleChatMessage

class GroupChat(AsyncWebsocketConsumer):
  async def connect(self):
    self.user = self.scope["user"]
    self.group_id = self.scope["url_route"]["kwargs"]["id"]
    self.group_chat_id = f'group_{self.group_id}'
    
    await self.accept()
    await self.channel_layer.group_add(self.group_chat_id,self.channel_name)
  
  async def send_response(self,room,**kwargs):
    return await self.channel_layer.group_send(room,{
      "type":"group_chat",
      "text" : json.dumps(kwargs)
    })
  
  
  async def receive(self,text_data):
    data = json.loads(text_data)
    
    if data["type"] == "delete":
      await self.delete_msg(data["msgId"])
      await self.update_last_msg()
      await self.send_response(self.group_chat_id,**data)
      return 
    
    if data["type"] == "message":
      await self.create_group_msg(data["msg"])
      await self.update_last_msg()
      msg = await self.get_latest_message()
      
      await self.send_response(self.group_chat_id,**msg)
      return 
    
    if data["type"] == "reply":
      
      data = await self.reply_msg(data["msgId"],data["msg"])
      await self.update_last_msg()
      await self.send_response(self.group_chat_id,**data)
    
    if data["type"] == "edit":
      await self.edit_msg(data["msgId"],data["msg"])
     
      await self.send_response(self.group_chat_id,**data)
      return 

    
   
  @database_sync_to_async 
  def delete_msg(self,id):
    msg= GroupMessage.objects.filter(id=id)
    if msg.exists():
      msg.first().delete()
      return True
    return False
  
  @database_sync_to_async 
  def create_group_msg(self,msg):
    group = Group.objects.get(id=self.group_id)
    GroupMessage.objects.create(group=group,message=msg,user=self.user)
  
  @database_sync_to_async 
  def reply_msg(self,msg_id,msg):
    group = Group.objects.get(id=self.group_id)
    message = GroupMessage.objects.filter(id=msg_id)
    if message.exists():
      msg = GroupMessage(group=group,message=msg,reply=message.first(),user=self.user)
      msg.save()
      rep_data = {
        "msg":msg.message ,
        "reply_to":msg.reply.message,
        "sent_by":self.user.username,
        "msg_id":msg.id,
        "type":"reply",
        "name":f"{self.user.first_name} {self.user.last_name}"
        
      }
      return rep_data

    return 
   
  @database_sync_to_async 
  def edit_msg(self,msg_id,new_msg):
    message = GroupMessage.objects.get(id=msg_id)
    message.message = new_msg 
    message.save()
    return True
    
  @database_sync_to_async 
  def get_latest_message(self):
    data = GroupMessage.objects.filter(user=self.user).latest("id")
    data = {"msg_id":data.id,"msg":data.message,"sent_by":self.user.username,"type":"message","name":f"{self.user.first_name} {self.user.last_name}"}
    return  data
  
  async def group_chat(self,event):
    await self.send(json.dumps({
      "type":"websocket.send",
      "text":event["text"]
    }))
  
  @database_sync_to_async 
  def update_last_seen(self):
    user = self.user
    user.last_seen = timezone.now()
    user.save()
    
  @database_sync_to_async 
  def update_last_msg(self):
    group = Group.objects.get(id=self.group_id)
    last = GroupMessage.objects.filter(group=group).last()
    if last:
      group.recent_msg = last.message
      group.save()
      return 
    group.recent_msg = "No Messages"
    group.save()
    
    
  
  async def disconnect(self,code):
    await self.update_last_seen()
    await self.channel_layer.group_discard(self.group_chat_id,self.channel_name)
    await self.close()


class SingleChatConsumer(AsyncWebsocketConsumer):
  
  async def connect(self):
    self.user = self.scope["user"]
  
    self.other_username = self.scope["url_route"]["kwargs"]["username"]
    self.chat_room = f"{self.user.username}_and_{self.other_username}"
    await self.accept()
    await self.channel_layer.group_add(self.chat_room,self.channel_name)

  
  async def send_response(self,room,**kwargs):
    await self.channel_layer.group_send(room,{
      "type":"chat_message",
      "text" : json.dumps(kwargs)
    })

  async def receive(self,text_data):
    data = json.loads(text_data)
    
    user_2 = await self.get_user(self.other_username)
    
    if data["type"] == "clear_history":
      await self.clear_history(user_2)
      await self.update_recent_msg(user_2)
      await self.send_response(self.chat_room,**data)
      await self.send_response(f"{self.other_username}_and_{self.user.username}",**data)
      return 
    
    
    if data["type"] == "edit":
      await self.edit_msg(data["msgId"],data["msg"])
      await self.send_response(self.chat_room,**data)
     
      
      await self.send_response(f"{self.other_username}_and_{self.user.username}",**data)
      return 
    
    
    if data["type"] == "reply":
      rep_data = await self.reply_msg(data["msgId"],user_2,data["msg"])
      await self.update_recent_msg(user_2)

      await self.send_response(self.chat_room,**rep_data)
      
      await self.send_response(f"{self.other_username}_and_{self.user.username}",**rep_data)
      return 
    
    if data["type"] == "delete":
      await self.delete_msg(data["msgId"])
      await self.update_recent_msg(user_2)

      await self.send_response(self.chat_room,**data)

      await self.send_response(f"{self.other_username}_and_{self.user.username}",**data)
      return 
    
    new_msg_response = {
      "type":"message",
      "sent_by":self.user.id
    }
    
  
    await self.create_conversation(self.user,user_2)
    await self.create_message(self.user,user_2,data["msg"])
    await self.update_recent_msg(user_2)
    msg_data = await self.get_latest_message()
    await self.send_response(self.chat_room,**new_msg_response,**msg_data)
  
    await self.send_response(f"{self.other_username}_and_{self.user.username}",**new_msg_response,**msg_data)
  
  @database_sync_to_async 
  def get_latest_message(self):
    data = SCM.objects.filter(first_user=self.user).latest("id")
    data = {"msg_id":data.id,"msg":data.message}
    return  data
     
  @database_sync_to_async
  def create_conversation(self,user,user_2):
    return create_conversation(user,user_2)
    
  async def chat_message(self,event):
    message = event['text']
    await self.send(json.dumps({
      "type":"websocket.send",
      "text":message
    }))
            
    
  @database_sync_to_async
  def get_user(self,username):
    user = User.objects.get(username=username)
    return user 
    
    
  @database_sync_to_async
  def create_message(self,user,user2,message):
     return SCM.objects.create(first_user=user,second_user=user2,message=message)

  @database_sync_to_async 
  def delete_msg(self,id):
    msg= SCM.objects.filter(id=id)
    if msg.exists():
      msg.first().delete()
      return True
    return False
    
  @database_sync_to_async
  def reply_msg(self,id,user_2,msg):
    message = SCM.objects.filter(id=id)
    if message.exists():
      SCM.objects.create(first_user=self.user,second_user=user_2,message=msg,reply=message.first())
      latest = SCM.objects.filter(first_user=self.user).latest("id")
      rep_data = {
        "msg":latest.message ,
        "reply_to":latest.reply.message,
        "sent_by":self.user.id,
        "msg_id":latest.id,
        "type":"reply"
        }
      
      
      return rep_data
    return
  
  @database_sync_to_async
  def clear_history(self,user2):
    msgs = [i.delete() for i in SCM.objects.filter(Q(first_user=self.user,second_user=user2)|Q(first_user=user2,second_user=self.user))]
    return 
    
  
  @database_sync_to_async 
  def edit_msg(self,id,new_msg):
    message = SCM.objects.filter(id=id)
    if message.exists():
      message = message.first()
      message.message = new_msg 
      message.save()
      return True 
    return False 
  
  @database_sync_to_async 
  def update_last_seen(self):
    user = self.user 
    user.last_seen = timezone.now()
    user.save()
    
  @database_sync_to_async 
  def update_recent_msg(self,user2):
    last = SCM.objects.filter(Q(first_user=self.user,second_user=user2) | Q(first_user=user2,second_user=self.user)).last()
    user = SingleChat.objects.filter(user_1=self.user,user_2=user2)
      
    second_user = SingleChat.objects.filter(user_1=user2,user_2=self.user)
    
    if last:
      if second_user:
        second_user = second_user.first()
        second_user.recent_msg=last.message
        second_user.save()
      if user:
        user = user.first()
        user.recent_msg = last.message
        user.save()
      return 
    
    last_msg = "No Message"
    if user:
      user = user.first()
      user.recent_msg = last_msg 
      user.save()
    if second_user:
      second_user = second_user.first()
      second_user.recent_msg=last_msg
      second_user.save()
    return 
    

  
  async def disconnect(self,close_code):
    await self.update_last_seen()
    await self.channel_layer.group_discard(self.chat_room,self.channel_name)
    await self.close()
     
