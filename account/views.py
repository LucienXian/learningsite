from django.shortcuts import render, render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from account.models import User

from .forms import UserForm
import pdb

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    message = "请检查填写的内容！"
    #pdb.set_trace()
    if request.method == 'POST':
        #pdb.set_trace()
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            filterResult = User.objects.filter(username = username)
            if len(filterResult)>0:
                return render(request,'register.html',{"errors":"用户名已存在"})
            elif form.cleaned_data.get('password') != form.cleaned_data.get('confirmedpassword'):
                errors = []
                errors.append("两次输入的密码不一致!")
                return render(request,'register.html',{'errors':errors})
            password = form.cleaned_data.get('password')
            email = form.cleaned_data['email']
            user = User(username=username,password=password,email=email)
            user.save()
            return render(request,'success.html',{'operation':"注册"})
        else:
            return render(request,'register.html',{'form': form})
    else:
        return render(request, 'register.html')

def forgot(request):
    return render(request, 'forgot.html')