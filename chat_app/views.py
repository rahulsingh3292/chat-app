from django.shortcuts import render,redirect ,HttpResponse 
from django.http import JsonResponse
from  .models import (User,SingleChatMessage,SingleChat,Group,GroupMessage,Contact )
from django.core import serializers
from  .decorators import restrict_self_chat,group_member_required
from django.db.models import Q 
from  .helpers import check_user_exists
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q 
# Create your views here.

SCM = SingleChatMessage 


@login_required
def home(request):
  chats = SingleChat.objects.filter(user_1=request.user)
  context = {"chats":chats}
  return render(request,"chat/chat.html",context)
  
@login_required
@restrict_self_chat
def single_chat(request,**kwargs):
  user = User.objects.get(username=kwargs.get("username"))
  msgs = SCM.objects.filter(Q(first_user=request.user,second_user=user)|Q(first_user=user,second_user=request.user)).order_by("timestamp")
  
  context = {"user":user,"msgs":msgs}
  return render (request,"chat/chat-view.html",context)
  
@login_required
def group_home(request):
  user = request.user 
  groups = [g for g in Group.objects.all() if (g.users.filter(id=user.id).exists() or g.admin == request.user)]
  return render(request,"chat/group.html",{"groups":groups})

@login_required
def group_add(request):
  if request.method == "POST":
    admin = request.user
    name = request.POST.get("name")
    description = request.POST.get("description")
    members = request.POST.getlist("member")
    group = Group(name=name,description=description,admin=admin)
    group.save()
    if members:
      for user_id in members:
        user = User.objects.get(id=user_id)
        group.users.add(user)
      group.save()
    return redirect(f"/group/{group.id}/")
  contacts = Contact.objects.get(user=request.user).contact_users.all()
  return render(request,"chat/add-group.html",{"contacts":contacts})
  
@login_required
@group_member_required
def group_chat(request,id):
  group = Group.objects.get(id=id)
  msgs = GroupMessage.objects.filter(group=group).order_by("timestamp")
  context = {"group_msgs":msgs,"group":group}
  return render(request,"chat/chat-view-group.html",context )
  
@login_required
@group_member_required
def group_profile(request,id):
  group = Group.objects.get(id=id)
  members = group.users.all()
  context ={"group":group,"members":members}
  return render(request,"chat/group-profile.html",context)
  



@login_required
def profile(request):
  return render(request,"chat/profile.html")
  
@login_required
def other_user_profile(request,username):
  user = check_user_exists(username)
  if user:
    if user == request.user:
      return redirect("/profile/")
    is_in_contact= Contact.objects.get(user=request.user).contact_users.filter(id=user.id).exists()
    
    context = {"user":user,"is_in_contact":is_in_contact}
    return render(request,"chat/other_profile.html",context)
  return redirect ("/")
  
@login_required
@csrf_exempt
def contacts(request):
  if request.method == "POST":
    user_id = request.POST.get("user_id")
    user = User.objects.get(id=user_id)
    contact = Contact.objects.get(user=request.user)
    contact.contact_users.add(user)
    contact.save()
    
    return JsonResponse({"status":200})
  
  contacts = Contact.objects.get(user=request.user).contact_users.all()
 
  return render(request,"chat/contacts.html",{"contacts":contacts})

@csrf_exempt
def upload_file(request):
  if request.method == "POST":
    file = request.FILES.get("file")
    user = request.user 
    storage = user.photo.storage 
    if user.photo:
        storage.delete(file.name)
    user.photo = file
    user.save() 
    return JsonResponse({"status":user.photo.url})
  return redirect("/")
    
@csrf_exempt
def upload_group_photo(request):
  if request.method == "POST":
    file = request.FILES.get("file")
    group = Group.objects.get(id=request.POST["g_id"])
    storage = group.logo.storage 
    if group.logo:
        storage.delete(file.name)
    group.logo = file
    group.save() 
    return JsonResponse({"status":group.logo.url})
  return redirect("/")    
    
@csrf_exempt 
def update_group(request,id):
  if request.method == "POST":
    name = request.POST["group_name"]
    bio = request.POST["bio"]
    group = Group.objects.get(id=id)
    group.name = name 
    group.description = bio 
    group.save()
    return JsonResponse({"status":True})
  return redirect("/")


@csrf_exempt
def edit_profile(request):
  if request.method == "POST":
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    username = request.POST["username"]
    bio = request.POST["bio"]
    user = check_user_exists(username)
    if user:
      if user != request.user:
        return JsonResponse({"status":False})
      
    user = request.user 
    user.first_name = first_name 
    user.last_name = last_name 
    user.username = username 
    user.bio = bio 
    user.save()
    return JsonResponse({"status":True})
    
  return redirect("/")
  
  
@login_required
def search_users(request):
  username = request.GET.get("username")
  if username:
    users= User.objects.filter(username__startswith=username).exclude(username=request.user.username)
    data = serializers.serialize("json",users)
    return JsonResponse({"data":data})
  return render(request,"chat/search_users.html")


def exit_group(request,id):
  group = Group.objects.get(id=id)
  group.users.remove(request.user)
  group.save()
  return redirect("/group/")
    
def delete_group(request,id):
  group = Group.objects.get(id=id)
  group.delete()
  msgs = [i.delete() for i in GroupMessage.objects.filter(group=group)]
  return redirect("/group/")

def delete_chat(request,username):
  user = check_user_exists(username)
  if user:
    chat = SingleChat.objects.filter(user_1=request.user,user_2=user)
    if chat:
      msgs =[i.delete() for i in SCM.objects.filter(first_user=request.user,second_user=user)]
      chat.first().delete()
    return redirect("/")
  return redirect("/")
    
def delete_chat_from_both(request,username):
  user = check_user_exists(username)
  if user:
    chat1 = SingleChat.objects.filter(user_1=request.user,user_2=user)
    chat2 = SingleChat.objects.filter(user_1=user,user_2=request.user)
    msgs = [i.delete() for i in SCM.objects.filter(Q(first_user=request.user,second_user=user)|Q(first_user=user,second_user=request.user)) ]
    if chat1: 
      chat1.first().delete()
    
    if chat2:
      chat2.first().delete()
    
    return redirect("/")
  return redirect("/")
  