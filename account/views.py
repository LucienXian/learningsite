from django.shortcuts import render, render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password


from .forms import UserForm, UserFormLogin
# import pdb

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        form = UserFormLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            userResult = User.objects.filter(email=email)
            if userResult:
                p = User.objects.get(email=email)
                ps_bool = check_password(password, p.password)
                #user = authenticate(request, email=email)
                if ps_bool:
                    auth.login(request, p)
                    request.session['username'] = p.username
                    return render(request,'success.html',{'operation':"登录"})
                else:
                    return render(request,'login.html',{"errors":"密码错误"})
            else:
                return render(request,'login.html',{"errors":"邮箱不存在"})
        else:
            return render(request,'login.html',{'errors': "请检查填写的内容！"})
    else:
        return render(request, 'login.html')

def register(request):
    message = "请检查填写的内容！"
    #pdb.set_trace()
    if request.method == 'POST':
        #pdb.set_trace()
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')                        
            username = form.cleaned_data['name']
            filterResult = User.objects.filter(email = email)

            if len(filterResult)>0:
                return render(request,'register.html',{"errors":"邮箱已存在"})
            elif form.cleaned_data.get('password') != form.cleaned_data.get('confirmedpassword'):
                errors = []
                errors.append("两次输入的密码不一致!")
                return render(request,'register.html',{'errors':errors})
            password = form.cleaned_data.get('password')
            
            user = User(username=username,password=make_password(password),email=email)
            user.save()
            return render(request,'success.html',{'operation':"注册"})
        else:
            return render(request,'register.html',{'form': message})
    else:
        return render(request, 'register.html')

def forgot(request):
    return render(request, 'forgot.html')