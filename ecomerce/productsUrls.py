from django.urls import path
from . import productsViews


urlpatterns = [
   
    
    path('products',productsViews.AllProducts,name ='products'),
    path('shop',productsViews.ShopProducts,name ='shop'),
    path('addproduct',productsViews.AddProducts,name ='addproduct'),
    path('editproduct/<int:product_id>/',productsViews.EditProducts,name ='editproduct'),
    path('product/<int:product_id>/',productsViews.ViewProduct,name ='product'),
    path('deleteproduct/<int:product_id>/',productsViews.DeleteProducts,name ='deleteproduct'),
]