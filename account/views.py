from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def forgot(request):
    return render(request, 'forgot.html')