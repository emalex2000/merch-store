from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_auth_app.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'Placeholder':'Username'})) 
    email = forms.EmailField(widget=forms.EmailInput(attrs={'Placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'Placeholder':'Input Password...'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'Placeholder':'Repeat Password...'}))
    class Meta:
        model = User
        fields = ['username', 'email',]