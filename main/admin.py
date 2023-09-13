from django.contrib import admin
from .models import *
from .e_models import *
# Register your models here.
class RegisterAdminModel(admin.ModelAdmin):
    list_display=('title','email','password')
admin.site.register(Company,RegisterAdminModel)

# Job Model
class JobAdminModel(admin.ModelAdmin):
    list_display=('company','title','publish','post_date')
admin.site.register(Job,JobAdminModel)

# Employee Model
class EmployeeAdminModel(admin.ModelAdmin):
    list_display=('full_name','job_title','email','active_status')
admin.site.register(Employee,EmployeeAdminModel)

# Applied Jobs
class ApplyJobAdmin(admin.ModelAdmin):
    list_display=('job','company','employee','applied_time','status')
admin.site.register(ApplyJob,ApplyJobAdmin)

# Notification
class NotificationAdmin(admin.ModelAdmin):
    list_display=('ref_type','read_status')
admin.site.register(Notification,NotificationAdmin)