from django.urls import include, path

from . import views

app_name = 'account'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgot/', views.forgot, name='forgot'),
    path('learn/', include('learn.urls')),
]