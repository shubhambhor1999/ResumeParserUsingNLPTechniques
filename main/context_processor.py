from .models import Notification,Company
def company_noti_count(request):
    total_notification=0
    if 'companyId' in request.session:
        company=request.session['companyId']
        total_notification=Notification.objects.filter(receiver_id=company).count()
    return {'totalNotification':total_notification}