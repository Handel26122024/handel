from django.urls import path
from . import stockViews as views

urlpatterns = [
    path('create_purchase/', views.create_purchase, name='create_purchase'),
    path('purchases/', views.PerchasesView, name='purchases'),
    path('add_purchase_item/<str:purchase_number>/', views.add_purchase_item, name='add_purchase_item'),
    path('edit_purchase_item/<str:item_id>/', views.edit_purchase_item, name='edit_purchase_item'),
    path('edit_purchase_item/<str:item_id>/', views.edit_purchase_item, name='edit_purchase_item'),
    path('delete_purchase_item/<str:item_id>/', views.delete_purchase_item, name='delete_purchase_item'),
    
    path('add_operation_cost/<str:purchase_number>/', views.add_operation_cost, name='add_operation_cost'),
    path('edit_operation_cost/<str:pk>/', views.edit_operation_cost, name='edit_operation_cost'),
    path('delete_operation_cost/<str:pk>/', views.delete_operation_cost, name='delete_operation_cost'),
    
    path('add_damage_report/<str:purchase_number>/', views.add_damage_report, name='add_damage_report'),
    path('edit_damage_report/<str:damage_id>/', views.edit_damage_report, name='edit_damage_report'),
    path('delete_damage_report/<str:damage_id>/', views.delete_damage_report, name='delete_damage_report'),
    
    path('purchase/<str:purchase_number>/', views.purchase_detail, name='purchase_detail'),
    path('lock_purchase/<str:purchase_number>/', views.lock_purchase, name='lock_purchase'),
    path('stock_level/', views.StockLevelView, name='stock_level'),
]
