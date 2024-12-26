from django.urls import path
from . import businessViews
from . import staffViews
from . import rolesViews

urlpatterns = [
   
    
    path('newbusiness',businessViews.NewBusiness,name ='newbusiness'),
    path('business',businessViews.businessProfile,name ='business'),
    path('editbusiness',businessViews.editBusiness,name ='editbusiness'),
    path('deletebusiness',businessViews.deleteBusiness,name ='deletebusiness'),
    
    path('addlocation',businessViews.NewBusinessLocation,name ='addlocation'),
    path('editlocation/<int:location_id>/',businessViews.editBusinessLocation, name='editlocation'),
    path('deletelocation/<int:location_id>/',businessViews.deleteBusinesslocation, name='deletelocation'),
    
    path('addorderstatus',businessViews.NewOrderStatus,name ='addorderstatus'),
    path('editaddorderstatus/<int:orderstatus_id>/',businessViews.EditOrderStatus, name='editaddorderstatus'),
    path('deleteaddorderstatus/<int:orderstatus_id>/',businessViews.deleteOrderStatus, name='deleteaddorderstatus'),
    
    
    path('allstaff',staffViews.AllStaff,name ='allstaff'),
    path('singlestaff',staffViews.SingleStaff,name ='singlestaff'),
    
    
    
    path('roles',rolesViews.AllRoles,name ='roles'),
    path('role/<int:role_id>/',rolesViews.SingleRole,name ='role'),
    path('newrole',rolesViews.NewRole,name ='newrole'),
    path('editrole/<int:role_id>/',rolesViews.EditRole, name='editrole'),
    path('deleterole/<int:role_id>/',rolesViews.DeleteRole, name='deleterole'),
    path('assignstaff/<int:role_id>/',rolesViews.AssignStaff, name='assignstaff'),
    path('removestaff/<int:staff_id>/',rolesViews.RemoveStaff, name='removestaff'),
    
    
    path('recentbusinesses',businessViews.RecentBusinesses,name ='recentbusinesses'),
    
    path('switch_business_status/', businessViews.Switch_Business_status, name='switch_business_status'),
    path('remove_business/', businessViews.remove_business, name='remove_business'),
]