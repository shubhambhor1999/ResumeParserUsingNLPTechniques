from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib import messages
from django.core import serializers
from .models import *
from .e_models import *
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail


# Home Page
def index(request):
    return render(request,'Home.html')
# Contact Us
def contact(request):
    return render(request,'contact.html')
# Contact Us
def about(request):
    return render(request,'about.html')
# Jobs List
def jobs(request):
    page = request.GET.get('page', 1)
    if 'search' in request.GET:
        search=request.GET['search']
        jobs=Job.objects.filter((Q(title__icontains=search)|Q(detail__icontains=search)) & Q(publish=True)).order_by('-id')
    else:
        jobs=Job.objects.filter(Q(publish=True)).order_by('-id')
    paginate=Paginator(jobs,10)
    jobs=paginate.page(page)
    return render(request,'jobs.html',{'jobs':jobs})


# Job Detail
def job_detail(request,job_id):
    applied=False
    job=get_object_or_404(Job,id=job_id)
    if 'empLogin' in request.session:
        emp=Employee.objects.get(pk=request.session['empId'])
        checkApplied=ApplyJob.objects.filter(employee=emp,job=job).count()
        if checkApplied>0:
            applied=True
    return render(request,'job-detail.html',{'job':job,'applied':applied})

# Job Apply
def job_apply(request):
    if 'empLogin' in request.session:
        if request.method=='POST':
            job=Job.objects.get(pk=request.POST['job_id'])
            company=Company.objects.get(pk=request.POST['company_id'])
            emp=Employee.objects.get(pk=request.POST['emp_id'])
            ApplyJob.objects.create(
                job=job,
                company=company,
                employee=emp
            )
            user_id=request.POST['emp_id']
            ref_id=request.POST['job_id']
            # Create Notification
            Notification.objects.create(
                user_id=request.POST['emp_id'],
                receiver_id=request.POST['company_id'],
                ref_type='job_apply',
                ref_id=request.POST['job_id'],
                ref_content='<a href="/p/profile/{0}">{1}</a> has applied on <a href="/job/detail/{2}">{3}</a>'.format(user_id,emp.full_name,ref_id,job.title),
            )
            messages.success(request, 'You have successfully applied.')
            return redirect('/job/detail/'+str(request.POST['job_id']))
    else:
        return redirect('/login')
'''
Company Section Start
'''

# Company List
def company_list(request):
    page = request.GET.get('page', 1)
    if 'search' in request.GET:
        search=request.GET['search']
        companies=Company.objects.filter((Q(title__icontains=search)|Q(detail__icontains=search)) & Q(active_status=True)).order_by('-id')
    else:
        companies=Company.objects.all()
    paginate=Paginator(companies,9)
    companies=paginate.page(page)
    return render(request,'company/list.html',{'companies':companies})

# Company Detail
def company_detail(request,id):
    company=get_object_or_404(Company,id=id)
    jobs=Job.objects.filter(company=company,publish=True)
    return render(request,'company/detail.html',{'company':company,'jobs':jobs})

# Register Company
def company_register(request):
    if 'companyLogin' in request.session:
        return redirect('/company/profile')
    if request.method=='POST':
        registerForm=CompanyRegisterForm(request.POST)
        if registerForm.is_valid():
            company=registerForm.save()
            company.save()
            messages.success(request, 'Company registred successfully.')
            return redirect('/company/register')
    else:
        registerForm=CompanyRegisterForm()
    return render(request,'company/register.html',{'form':registerForm})

# Login Company
def company_login(request):
    if 'companyLogin' in request.session:
        return redirect('/company/profile')
    if request.method=='POST':
        loginForm=CompanyLoginForm(request.POST)
        if loginForm.is_valid():
            email=loginForm.cleaned_data['email']
            password=loginForm.cleaned_data['password']
            check=Company.objects.filter(email=email,password=password).count()
            if check>0:
                company_data=Company.objects.get(email=email,password=password)
                request.session['companyLogin']=True
                request.session['companyId']=company_data.id
                return redirect('/company/profile')
            else:
                messages.info(request,'Invalid Email/Password!!')
    else:
        loginForm=CompanyLoginForm()
    return render(request,'company/login.html',{'form':loginForm})

# Company Logout
def company_logout(request):
    del request.session['companyLogin']
    del request.session['companyId']
    return redirect('/company/login')

# Profile Company
def company_profile(request):
    company=get_object_or_404(Company,id=request.session['companyId'])
    if request.method=='POST':
        registerForm=CompanyRegisterForm(request.POST,instance=company)
        if registerForm.is_valid():
            registerForm.save()
            messages.success(request,'Profile has been updated.')
            return redirect('/company/profile')
    registerForm=CompanyRegisterForm(instance=company)
    return render(request,'company/profile.html',{'form':registerForm})
    
# Company Job list
def company_jobs(request):
    company=Company.objects.get(pk=request.session['companyId'])
    jobs=Job.objects.filter(company=company).order_by('-id')
    return render(request,'company/job-list.html',{'jobs':jobs})

# Applied Jobs
def company_applied_jobs(request,id):
    job=get_object_or_404(Job,id=id)
    company=get_object_or_404(Company,id=request.session['companyId'])
    employees=ApplyJob.objects.filter(job=job,company=company)
    return render(request,'company/applied-list.html',{'employees':employees})

# Create Job
def post_job(request):
    if 'companyLogin' not in request.session:
        return redirect('login')
    if request.method=='POST':
        jobForm=PostJobForm(request.POST)
        if jobForm.is_valid():
            company = jobForm.save(commit=False)
            company.company=Company.objects.get(pk=request.session['companyId'])
            company.save()
            messages.success(request,'Job has been posted.')
            return redirect('/company/post-job')
    else:
        jobForm=PostJobForm()
    return render(request,'company/post-job.html',{'form':jobForm})

# Company Job Detail
def company_job_detail(request,job_id):
    detail=Job.objects.get(pk=job_id)
    return render(request,'company/job-detail.html',{'job':detail})

# Company Job Update
def company_job_update(request,job_id):
    job=get_object_or_404(Job, id=job_id)
    jobForm=PostJobForm(instance=job)
    if request.method=='POST':
        jobForm=PostJobForm(request.POST,instance=job)
        if jobForm.is_valid():
            company = jobForm.save(commit=False)
            company.company=Company.objects.get(pk=request.session['companyId'])
            company.save()
            messages.success(request,'Job has been updated.')
            return redirect('/company/jobs/update/'+str(job_id))
    detail=Job.objects.get(pk=job_id)
    return render(request,'company/job-update.html',{'job':detail,'form':jobForm})

# Delete Job f company
def company_job_remove(request,job_id):
    Job.objects.filter(pk=job_id).delete()
    return redirect('/company/jobs')

# Company Notification
def company_notifications(request):
    notifications=Notification.objects.filter(receiver_id=request.session['companyId']).order_by('-read_status')
    return render(request,'company/notifications.html',{'notifications':notifications})

def mail(request):
    return render(request,"company/mail.html")

def employee_notifications(request):
    print("hii")
    subject = request.GET['subject']
    email = request.GET['email']
    message = request.GET['message']
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
    messages.success(request, 'Mail Sent successfully.')
    return render(request, "company/mail.html")

'''
Company Section End
'''