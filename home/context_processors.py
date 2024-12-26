from django.contrib.auth.decorators import login_required

from business.models import RecentActiveBusiness
from ecomerce.models import Notification  # Assuming you have a Notification model
from django.db.models import Q

import datetime
from django.utils import timezone
from datetime import timedelta

def active_user(request):
    active_business = None  # To hold active business if found
    unseen_notifications_count = 0  # To hold unseen notifications count

    if request.user.is_authenticated:
        user = request.user
        # Get active business for the authenticated user
        try:
            active_business = RecentActiveBusiness.objects.get(visitor=user, active_status='On')
        except RecentActiveBusiness.DoesNotExist:
            active_business = None

        # Fetch unseen notifications for the user
        unseen_notifications_count = Notification.objects.filter(user=user, is_seen=False).count()

    return {
        'active_business': active_business,
        'unseen_notifications_count': unseen_notifications_count,
    }
    
    #OTHER DEFS WILL RETURN DICTIONARY LIKE CONTEXTS