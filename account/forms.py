from django import forms

class UserForm(forms.Form):
    name = forms.CharField(label='name',max_length=100)
    password = forms.CharField(label='password',widget=forms.PasswordInput())
    confirmedpassword = forms.CharField(label='confirmedpassword',widget=forms.PasswordInput())
    email = forms.EmailField(label='email')
