from  .models import User,SingleChat,Group 

def check_user_exists(username):
  user = User.objects.filter(username=username)
  if user.exists():
    return user.first()
  return False 


def create_conversation(user,user_2):
  check_user_1 = SingleChat.objects.filter(user_1=user,user_2=user_2).exists()
  if not check_user_1:
    SingleChat.objects.create(user_1=user,user_2=user_2)
  
  check_user_2 = SingleChat.objects.filter(user_1=user_2,user_2=user).exists()
  if not check_user_2:
    SingleChat.objects.create(user_1=user_2,user_2=user)
  return True 

  