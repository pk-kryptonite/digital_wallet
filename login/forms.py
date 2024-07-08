from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    first_name = forms.CharField(label='password', max_length=100)
    last_name = forms.CharField(label='password', max_length=100)
    email= forms.CharField(label='password', max_length=100)