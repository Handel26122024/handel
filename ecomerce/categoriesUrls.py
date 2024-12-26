from django.urls import path
from . import categoriesViews


urlpatterns = [
   
    
    path('categories',categoriesViews.Categories,name ='categories'),
    path('addcategory',categoriesViews.AddCategory,name ='addcategory'),
    path('editcategory/<int:pk>/',categoriesViews.EditCategory,name ='editcategory'),
    path('deletecategory/<int:pk>/',categoriesViews.DeleteCategory,name ='deletecategory'),
]