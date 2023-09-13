from django.db import models

# Company Register
class Company(models.Model):
    title=models.CharField(max_length=20)
    email=models.CharField(max_length=50,default='',null=True)
    password=models.CharField(max_length=20,default='',null=True)
    detail=models.TextField(blank=True)
    contact_no=models.CharField(max_length=15)
    website=models.CharField(max_length=100,default='',null=True)
    address=models.CharField(max_length=150)
    active_status=models.BooleanField(default=True)
    class Meta:
        verbose_name_plural='Companies'

    def __str__(self):
        return self.title

# Jobs
class Job(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    detail=models.TextField(blank=True)
    publish=models.BooleanField(default=True)
    post_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Notification
class Notification(models.Model):
    user_id=models.CharField(max_length=200,default='0')
    receiver_id=models.CharField(max_length=200,default='0')
    ref_type=models.CharField(max_length=200)
    ref_id=models.CharField(max_length=200)
    ref_content=models.CharField(max_length=200)
    read_status=models.BooleanField(default=False)

    def __str__(self):
        return self.ref_type