from django.urls import path

from . import views

urlpatterns = [
    path('wordbook/', views.wordbook, name='wordbook'),
    path('wordbook/wordbookunit', views.wordbookunit, name='wordbookunit'),
    path('wordbook/wordbookunit/wordlist', views.wordlist, name='wordlist'),
]