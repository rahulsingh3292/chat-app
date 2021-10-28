
from base64 import b64encode 
from django.core.mail import send_mail
from django.conf import settings 

def encrypt_email(email):
  encode = b64encode(email.encode("utf-8"))
  encrypted = encode.decode("utf-8")
  return encrypted


def send_activation_mail(email,username):
  to = [email]
  from_mail = settings.EMAIL_HOST_USER
  subject = "Account Activation For DreamsChat"
  body = f"Hey {username}, Click to the link Activate your Account \n http://localhost:8000/accounts/verify-account?email={encrypt_email(email)}"
  send_mail(subject,body,from_mail,to)

def forget_password_mail(email):
  to = [email]
  from_mail = settings.EMAIL_HOST_USER
  subject = "Forget Password for DreamsChat"
  body = f" Click The link Reset your password \n http:/localhost:8000/accounts/forget-password/?email={encrypt_email(email)}"
  send_mail(subject,body,from_mail,to)
