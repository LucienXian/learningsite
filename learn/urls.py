from django.urls import path

from . import views

app_name = 'learn'

urlpatterns = [
    path('wordbook/', views.wordbook, name='wordbook'),
    path('wordbook/wordbookunit', views.wordbookunit, name='wordbookunit'),
    path('wordbook/wordbookunit/wordlist', views.wordlist, name='wordlist'),
    path('wordbook/mine', views.mywordbook, name='mywordbook'),
    path('learnindex/', views.learnindex, name='learnindex'),
    path('bdcsetting/', views.bdcsetting, name='bdcsetting'),
    path('learnindex/learnwords', views.learnwords, name='learnwords'),
    path('handleselfword/', views.handleselfword, name='selfword'),
    path('mywords/', views.mywords, name='mywords'),
    path('voctest/', views.voctest, name='voctest'),
    path('logout/', views.logout_view, name='logout'),
]