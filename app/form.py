from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()
from .models import Blogging

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

class SignupForm(forms.Form):

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=128)
    email = forms.EmailField()
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=200, widget=forms.PasswordInput())


    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This email is taken")
        return self.cleaned_data['email']

        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError("This username is taken")
        return self.cleaned_data['username']

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Your password didnot match ")



class BlogForm(ModelForm):
    class Meta:
        model = Blogging
        fields = ['title', "blog_details"]

class UserUpdate(ModelForm):
    # password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    # confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["first_name", "last_name"]

    # def clean(self):
    #     password = self.cleaned_data['password']
    #     confirm_password = self.cleaned_data['confirm_password']
    #     if password != confirm_password:
    #         raise forms.ValidationError("Your password didnot match ")