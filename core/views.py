from django.shortcuts import render,redirect
from .models import Contact,Category,Momo,Review
import qrcode
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import re
# Create your views here.
# @login_required(login_url="log_in")
def index(request):
    category=Category.objects.all()
    cateid=request.GET.get('category') #"2","all"
    # print(cateid)
    # print(type(cateid))
   
    if cateid == 'all':
        momo=Momo.objects.filter(is_available=True)
 
    elif cateid:
        
        momo=Momo.objects.filter(is_available=True,category=cateid)
    else:
        momo=Momo.objects.filter(is_available=True)
    if request.method== 'POST':
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        message=request.POST['message']
        Contact.objects.create(name=name,email=email,phone=phone,message=message)
        # request.session["name"]=name
        response= redirect('index')
        response.set_cookie('name',name,max_age=3600)
        return response
    
    context={
        'category':category,
        "momo":momo
        }
    return render(request,'core/index.html',context)
def about(request):
    return render(request,'core/about.html')
def contact(request):
    
    return render(request,'core/contact.html')

@login_required(login_url='log_in')
def menu(request):
    category=Category.objects.all()
    qr=qrcode.make("http://127.0.0.1:8000/menu/")
    qr.save("core/static/images/qr.png")
    
    context={
        'category':category
    }
    return render(request,'core/menu.html',context)
def service(request):
    return render(request,'core/services.html')

@login_required(login_url='log_in')
def testemonial(request):
    momos=Momo.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        message=request.POST['message']
        order=request.POST['order']
        rating=request.POST['rating']
        
        Review.objects.create(name=name,message=message,order=order,rating=rating)
        return redirect("testemonial")
    return render(request,'core/testemonial.html',{'momos':momos})

'''
Authentication(who are you?) : verify identity of user (login,register,logout)
Authorization  (what are you allowed to do ): the process of authencated user has permission to access

'''
'''
==================================================================
==================================================================
                    Auth Part
==================================================================
==================================================================
'''
def register(request):
    if request.method == 'POST':
        fname=request.POST['fname'] #sujan
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password'] #abc
        password1=request.POST['password1'] #xyz
        
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.error(request,"username is already exists")
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request,"email is already exists")
                return redirect('register')
            
            if not re.search(r"[A-Z]",password):
                messages.error(request,"password must contain at least one upper case")
                return redirect('register')
            if not re.search(r"\d",password):
                messages.error(request,"password must contain at least one digit")
                return redirect('register')
                
            try:
                user=User(first_name=fname,username=username)
                validate_password(password,user=user) #validation error : common ,length
                User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                messages.success(request,"your account is successfully register")
                return redirect('register')
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request,i)
                return redirect("register")
                
        else:
            messages.error(request,"password and confirm password doesnot match")
            return redirect('register')
            
        
    return render(request,'auth/register.html')
def log_in(request):
    name=request.COOKIES.get('name')
    if request.method == "POST":
        username=request.POST.get("username") #sujan710
        password=request.POST.get("password") #ram
        remember_me=request.POST.get('remember_me') #on / None
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,"username is not register yet")
            return redirect("log_in")
        
        user=authenticate(username=username,password=password) #user=sujan710 , user=NOne
        
        if user is not None:
            login(request,user)
            if remember_me:
                request.session.set_expiry(360000)
            else:
                request.session.set_expiry(0)
            next=request.POST.get('next',"") #/menu/           
            return redirect(next if next else 'index')
        else:
            messages.error(request,'Invalid Password')
            return redirect("register")
            
    next=request.GET.get('next',"")   #/testemonial/ 
        
    return render(request,'auth/login.html',{'next':next,"name":name})


def log_out(request):
    logout(request)
    return redirect('log_in')




'''
Cookies :
a small piece of data store in user's browser by server

it is used store in client side 
expiry date
storage limit (4kb per cookies)
user preferece


Session :

'''
@login_required(login_url="log_in")
def password_change(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("log_in")
    
    return render(request,'auth/password_change.html',{'form':form})


# pip freeze > requirements.txt
# pip install -r requirements.txt