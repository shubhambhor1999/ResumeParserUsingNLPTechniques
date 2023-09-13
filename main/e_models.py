from django.db import models
from .models import Company,Job
# Employee Model
class Employee(models.Model):
    full_name=models.CharField(max_length=200)
    job_title=models.CharField(max_length=200,default='')
    email=models.CharField(max_length=200,default='',null=True)
    password=models.CharField(max_length=200,default='',null=True)
    detail=models.TextField(blank=True)
    contact_no=models.CharField(max_length=200)
    address=models.CharField(max_length=300)
    resume=models.FileField(null=True)
    active_status=models.BooleanField(default=True)
    public=models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

# Apply Jobs
class ApplyJob(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True)
    company=models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    job=models.ForeignKey(Job,on_delete=models.SET_NULL,null=True)
    status=models.BooleanField(default=True)
    applied_time=models.DateTimeField(auto_now_add=True)
