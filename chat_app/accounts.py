from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.generic import TemplateView,CreateView
from django.contrib.auth import (authenticate,login,logout)
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from  .forms import SignupForm
from  .extras import * 
from  .models import User 
from django.utils.decorators import method_decorator
from braces.views import AnonymousRequiredMixin
from django.contrib.auth.decorators import login_required 

class SignupView(AnonymousRequiredMixin,CreateView):
  form_class = SignupForm 
  authenticated_redirect_url = "/"
  model = User
  template_name = "accounts/signup.html"
  success_url = "/accounts/signup/"
  
  def form_valid(self,form):
    self.username = form.cleaned_data.get("username")
    self.email = form.cleaned_data.get("email")
    if User.objects.filter(email=self.email).exists() or User.objects.filter(username=self.username).exists():
      return JsonResponse({"status":False})
    self.obj  = form.save(commit=False)
    self.obj.is_active = False
    self.obj.password = make_password(self.obj.password)
    send_activation_mail(self.email,self.username)
    self.obj.save()
  
    return JsonResponse({"status":True})
    
 
  
class LoginView(AnonymousRequiredMixin,TemplateView):
  template_name = "accounts/login.html"
  authenticated_redirect_url= "/"
  def post(self,request):
    redirect_url = self.request.POST.get("next")
    email = self.request.POST.get("email")
    password = self.request.POST.get("password")
    user = User.objects.filter(email=email) 
    if user.exists():
      if user.first().is_active == False:
        return JsonResponse({"active":False})
      
    user = authenticate(self.request,email=email,password=password)
    if user is not None:
      login(self.request,user)
      if redirect_url:
        return JsonResponse({"redirect_to":redirect_url})
      return JsonResponse({"status":True})
    return JsonResponse({"status":False})
    

@csrf_exempt
def activate_account(request):
  if request.method == "POST":
    email = request.POST.get("email")
    user = User.objects.filter(email=email)
    if not user.exists():
      return JsonResponse({"activated":False})
    user = user.first()
    if user.is_active == False:
        user.is_active = True 
        user.save()
        return JsonResponse({"activated":True})
    else:
      return JsonResponse({"activated":False})
  if not request.GET.dict().get("email"):
    return redirect("/")
   
  return render(request,"accounts/activate.html")



def logout_user(request):
  logout(request)
  return redirect("/")


def forget_email_page(request):
  if request.method == "POST":
    email = request.POST.get("email").lower()
    user = User.objects.filter(email=email)
    if user.exists():
      forget_password_mail(email)
      return JsonResponse({"status":True})
    else:
      return JsonResponse({"status":False})
  return render(request,"accounts/forget_email.html")


def forget_password(request):
  if request.method == "POST":
    new_pass = request.POST.get("new_pass")
    email = request.POST.get("email")
    user = User.objects.get(email=email)
    user.set_password(new_pass)
    user.save()
    
    return JsonResponse({"status":True})
  return render(request,"accounts/forget_password.html")
  
