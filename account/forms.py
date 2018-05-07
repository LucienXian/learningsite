from django import forms

class UserForm(forms.Form):
    name = forms.CharField(label='name',max_length=100)
    password = forms.CharField(label='password',min_length=6,widget=forms.PasswordInput())
    confirmedpassword = forms.CharField(label='confirmedpassword',min_length=6,widget=forms.PasswordInput())
    email = forms.EmailField(label='email')

class UserFormLogin(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password',min_length=6,widget=forms.PasswordInput())
