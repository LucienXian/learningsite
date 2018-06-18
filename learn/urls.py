from django.urls import path

from . import views

urlpatterns = [
    path('wordbook/', views.wordbook, name='wordbook'),
]