from django import forms
from .models import *
from .e_models import *

class CompanyRegisterForm(forms.ModelForm):
    class Meta:
        model=Company
        fields='__all__'

class CompanyLoginForm(forms.Form):
    email=forms.CharField(max_length=200)
    password=forms.CharField(max_length=200,widget=forms.PasswordInput)

# Company Jobs
class PostJobForm(forms.ModelForm):
    class Meta:
        model=Job
        fields=('title','detail','publish')

# Employee Register Form
class EmployeeRegisterForm(forms.ModelForm):
    class Meta:
        model=Employee
        exclude=('active_status',)

class EmployeeLoginForm(forms.Form):
    email=forms.CharField(max_length=200)
    password=forms.CharField(max_length=200,widget=forms.PasswordInput)

class ContactForm(forms.Form):
    email_address = forms.EmailField(max_length = 150)
    Subject = forms.CharField(max_length = 50)
    message = forms.CharField(widget = forms.Textarea, max_length = 2000)   