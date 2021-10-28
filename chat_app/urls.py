from django.urls import path 
from  .import views 
from  .import accounts
urlpatterns = [
     path("",views.home),
     
     path("accounts/signup/",accounts.SignupView.as_view()),
     
     path("accounts/login/",accounts.LoginView.as_view()),
     
     path("accounts/logout/",accounts.logout_user),
     
     path("accounts/verify-account/",accounts.activate_account),
     
     path("accounts/forget-email/",accounts.forget_email_page),
     
     path("accounts/forget-password/",accounts.forget_password),
     
     path("chat/<str:username>/",views.single_chat),
     
     path('add-group/',views.group_add),
     path("group/<int:id>/",views.group_chat),
     
     path("group/",views.group_home),
     
     path("group_profile/<int:id>/",views.group_profile),
     
     path('update_group/<int:id>/',views.update_group),
     
     path("profile/",views.profile),
     
     path("upload/",views.upload_file),
     
     path("upload-group-photo/",views.upload_group_photo),
     
     path("user-profile/<str:username>/",views.other_user_profile),
    
     path("edit-profile/",views.edit_profile),
     
     path("contacts/",views.contacts),
     
     path("search_users/",views.search_users),
     
     path('exit_group/<int:id>/',views.exit_group),
     
     path('delete_group/<int:id>/',views.delete_group),
     
     path("delete_chat/<str:username>/",views.delete_chat),
     
     path("delete_chat_both/<str:username>/",views.delete_chat_from_both),
 
     
  ]