from functools import wraps  
from django.shortcuts import HttpResponse,redirect
from  .models import SingleChat,User,Group
from  .helpers import check_user_exists

def restrict_self_chat(view_func):
  @wraps(view_func)
  def check(request,**kwargs):
    
    if request.user.username == kwargs.get("username"):
      return redirect("/")
    
    user_exist=check_user_exists(kwargs.get("username"))
    if not user_exist:
      return redirect("/")
      
    return view_func(request,**kwargs)
  return check

def group_member_required(view_func):
  @wraps(view_func)
  def check_member(request,id,*args,**kwargs):
    group = Group.objects.filter(id=id) 
    if group.exists():
      group = group.first()
      
      if group.admin == request.user:
        return view_func(request,id,*args,**kwargs)
      
      elif group.users.filter(id=request.user.id).exists():
        return view_func(request,id,*args,**kwargs)
   
      return redirect("/")
      
    return redirect("/")
  return check_member 