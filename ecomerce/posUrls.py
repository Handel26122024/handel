from django.urls import path
from . import posViews


urlpatterns = [
   
    
    path('pos',posViews.Pos,name ='pos'),
    path('posorders',posViews.POSOrders,name ='posorders'),
    path('poscheckout',posViews.PosCheckout,name ='poscheckout'),
    
]