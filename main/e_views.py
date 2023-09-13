# Employee Views
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .forms import *
from django.db.models import Q
from .e_models import *
from .PDF2 import *
import os
from django.conf import settings
import numpy as np 
from django.conf import settings
from django.core.mail import send_mail
from resume_parser import resumeparse
import json
# Register
def register(request):
    if 'empLogin' in request.session:
        return redirect('/profile')
    if request.method=='POST':        
        registerForm=EmployeeRegisterForm(request.POST,request.FILES)

        if registerForm.is_valid():
 
            employee=registerForm.save()
            employee.save()
            messages.success(request, 'You have registred successfully.')
            return redirect('/register')
    else:
        form=EmployeeRegisterForm()
        return render(request,'register.html',{'form':form})


# Login
def login(request):
    if 'empLogin' in request.session:
        return redirect('/profile')
    if request.method=='POST':
        loginForm=EmployeeLoginForm(request.POST)
        if loginForm.is_valid():
            email=loginForm.cleaned_data['email']
            password=loginForm.cleaned_data['password']
            check=Employee.objects.filter(email=email,password=password).count()
            if check>0:
                emp_data=Employee.objects.get(email=email,password=password)
                request.session['empLogin']=True
                request.session['empId']=emp_data.id
                if 'next' in request.GET:
                    redirect('/')
                return redirect('/profile')
            else:
                messages.info(request,'Invalid Email/Password!!')
    else:
        loginForm=EmployeeLoginForm()
    return render(request,'login.html',{'form':loginForm})
# Employee Logout
def logout(request):
    del request.session['empLogin']
    del request.session['empId']
    return redirect('/login')
# Profile
def profile(request):
    emp=get_object_or_404(Employee,id=request.session['empId'])
    if request.method=='POST':
        registerForm=EmployeeRegisterForm(request.POST,request.FILES,instance=emp)
        print(registerForm)
        if registerForm.is_valid():

            registerForm.save()
            messages.success(request,'Profile has been updated.')
            return redirect('/profile')
    registerForm=EmployeeRegisterForm(instance=emp)
    return render(request,'profile.html',{'form':registerForm})

def ranker(request):
    return render(request,'ranker.html')


def rank(request):
    fulltext = request.GET['fulltext']
    f=open('1.txt','w')
    f.write('\n')
    f.write(str(fulltext))
    f.close()
    os.system('python ranker.py --dir="D:\sem 7 sem 8 projects\Django-Job-Portal-Website-master\Hirex\media" --keyword-file="1.txt" --output-type="csv" --output-file="2.csv" --rename="NO"')
    import matplotlib
    import matplotlib.pyplot as plt
    import csv
    col_list = ["Percentile", "File Name","Total Count"]
    df = pd.read_csv("2.csv", usecols=col_list)
    print(df["Percentile"])
    x = []
    y = []
    
    x=df["File Name"]
    y=df["Percentile"]
    q=df["Total Count"]
    plt.figure()
    plt.bar(x, y, color = 'g', width = 0.2, label = "Candidate")
    plt.xticks(rotation=30, ha='right')
    plt.xlabel('Resumes')
    plt.ylabel('Percentage')
    plt.title('Resumes Ranked According to Keywords')
    plt.legend()
    z=settings.MEDIA_ROOT
    z=os.path.join(z,'files')
    files = ['books_read.png', 'rank.png', 'rank1.png']
    for f in files:
        p=os.path.join(z,str(f))
        os.remove(p)
    plt.savefig("books_read.png",bbox_inches = "tight")
    plt.clf
    plt.figure()
    plt.clf
    plt.pie(y,labels = x,autopct = '%.2f%%')
    plt.title('Resume Rank', fontsize = 20)
    plt.savefig('rank.png',bbox_inches = "tight")
    plt.clf
    plt.figure()
    plt.clf
    plt.bar(x, q, color = 'b', width = 0.2, label = "Candidate")
    plt.xticks(rotation=30, ha='right')
    plt.xlabel('Resumes')
    plt.ylabel('Count')
    plt.title('Resumes Ranked According to Keywords')
    plt.legend()
    plt.savefig('rank1.png',bbox_inches = "tight")
    import shutil
    files = ['books_read.png', 'rank.png', 'rank1.png']
    for f in files:
        shutil.move(f, str(z))
    return render(request,'ranks.html')


# Public Profile
def public_profile(request,id):
    emp=get_object_or_404(Employee,id=id,active_status=True,public=True)
    return render(request,'public-profile.html',{'emp':emp})

# emp Profile
def emp_profile(request,id):
    emp=get_object_or_404(Employee,id=id,active_status=True,public=True)
    return render(request,'emp-profile.html',{'emp':emp})

def parse(request,id):
    emp=get_object_or_404(Employee,id=id,active_status=True,public=True)
    print(emp)
    path=settings.MEDIA_ROOT
    print(path)
    d=emp.resume
    # this will return a tuple of root and extension
    split_tup = os.path.splitext(str(d))
    print(split_tup)
    
    file_extension = split_tup[1]

    z=os.path.join(path,str(d))
    data = resumeparse.read_file(str(z))
    if(file_extension=='.pdf'):
        text=extract_text_from_pdf(z)
    elif(file_extension=='.pdf'):
        text=extract_text_from_pdf(z)
    emails = extract_emails(text)
    phone_number = extract_phone_number(text)
    skillsfile=os.path.join(path,'skill1.csv')
    skills = extract_skill(text,skillsfile)
    education=extract_education(text)
    z=os.path.join(path,'files')
    file=os.path.join(z,"resume.txt")
    f = open(str(file), "w")
    f.write(text)   
    f.close()
    z=os.path.join(path,'files')
    # Serializing json 
    output= json.dumps(data, indent = 4)
    file=os.path.join(z,"resume1.txt")
    f = open(str(file), "w")
    f.write(output)
    f.close()
    context={
            'name':emp.full_name,
            'emails':emails,
            'skills':skills,
            'details':emp.detail,
            'address':emp.address,
            'phone':phone_number,
            'education':education,
            }       
    return render(request,'parse.html',context)


# Applied Jobs
def applied_jobs(request):
    emp=get_object_or_404(Employee,id=request.session['empId'])
    jobs=ApplyJob.objects.filter(employee=emp).order_by('applied_time')
    return render(request,'applied.html',{'jobs':jobs})
# Recommended Jobs
def recom_jobs(request):
    emp=get_object_or_404(Employee,id=request.session['empId'])
    jobs=Job.objects.filter(title__icontains=emp.job_title,publish=True).order_by('-id')
    return render(request,'recom.html',{'jobs':jobs})
# Messages

#resume Creation
def resume(request):
    return render(request,'resumegeneration.html')