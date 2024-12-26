from django.urls import path
from . import views


urlpatterns = [
   
    
    path('',views.Home,name ='home'),
    
    path('login',views.UserLogin,name ='login'),
    path('logout',views.UserLogout,name ='logout'),
    path('register',views.UserRegister,name ='register'),
    path('myprofile',views.UserProfile,name ='myprofile'),
    path('editprofile',views.EditUserProfile,name ='editprofile'),
    path('notifications',views.notification_list,name ='notifications'),
    
    
    
    path('changephonenumber/', views.change_phone_number, name='changephonenumber'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('changeusername/', views.change_username, name='changeusername'),
]