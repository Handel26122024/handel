from django.urls import path
from . import views


urlpatterns = [
   
    
    path('registerescort',views.register_escort,name ='registerescort'),
    path('ourescorts',views.escort_list,name ='ourescorts'),
    path('ourescort',views.escort_details,name ='ourescort'),
    path('escortrequest',views.escort_request_business,name ='escortrequest'),
    path('store_escort_id',views.store_escort_id,name ='store_escort_id'),
    
    path('escortrequests',views.EscortsRequetsList,name ='escortrequests'),
    
]