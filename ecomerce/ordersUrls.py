from django.urls import path
from . import ordersViews


urlpatterns = [
   
    
    path('onlineorders',ordersViews.Orders,name ='onlineorders'),
    
    path('order/<int:order_id>/',ordersViews.OrderView,name ='order'),
    path('editorder/<int:order_id>/',ordersViews.EditOrder,name ='editorder'),
    path('orderreport',ordersViews.SalesReport,name ='orderreport'),
    
    
    path('cart',ordersViews.Cart,name ='cart'),
    path('checkout',ordersViews.CheckOut,name ='checkout'),
    
    path('statusandstaff',ordersViews.SaveStaffandStatus,name ='statusandstaff'),
    path('myassignedorders',ordersViews.MyAssignedOrders,name ='myassignedorders'),
    path('myassignedorder/<int:order_id>/',ordersViews.MyAssignedOrderView,name ='myassignedorder'),
    path('status',ordersViews.SaveStatus,name ='status'),
    
    
    path('myorders',ordersViews.MyOrders,name ='myorders'),
    path('myorder/<int:order_id>/',ordersViews.MyOrderView,name ='myorder'),
    
    
    path('addpayement_proof/<int:order_id>/', ordersViews.AddPayementProofViews, name='addpayement_proof'),
    path('editpayement_proof/<int:payment_id>/', ordersViews.EditPayementProofViews, name='editpayement_proof'),
    path('confirmpayement/<int:proof_id>/', ordersViews.confirm_payment, name='confirmpayement'),
    path('rejectpayement/<int:proof_id>/', ordersViews.reject_payment, name='rejectpayement'),

    
]