from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

# User model not used
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):
        return self.user

    def save(self,*args,**kwargs):
        self.password = make_password(self.password) 
        super(User,self).save(*args,**kwargs)