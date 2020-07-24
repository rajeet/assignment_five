from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView


# for sending verification email

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode




# 

from .form import SignupForm, LoginForm, UserUpdate
from django.contrib.auth.views import LogoutView
# Create your views here.
from .models import Blogging, User

User = get_user_model()



def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print("form is valid")
            print(form.cleaned_data)
            print(request.POST)


            user = User(
            username=form.cleaned_data['username'],
            first_name = form.cleaned_data["first_name"],
            last_name = form.cleaned_data["last_name"],
            email = form.cleaned_data["email"],
            )
            user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('app/account_activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/account/profile/")
        form = SignupForm()
    return render(request, "app/signup.html", {"form":form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        print(request.POST['email'])
        if form.is_valid():
            print("form:" ,form.cleaned_data['email'])
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])

            # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(user)

            if user:
                print("A user is found")
                login(request, user)
                print(request.user)
                return redirect("/account/profile/")
            else:
                print("User invalid")
            print(form.cleaned_data)
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/account/profile/")
        form = LoginForm()

    return render(request, "app/login.html", {"form": form})

@login_required(login_url="/account/login/")
def profile_view(request):
    data = Blogging.objects.all()
    return render(request, "app/profile.html", {'blogs':data})


class Logout(LogoutView):
    template_name = "app/login.html"
    # logout view further to be edit



    # logout(request)
    # return redirect("/account/login/")

@login_required(login_url="/account/login/")
def editProfile(request):
    user_id = request.user.id
    print(user_id)
    user_object=instance=get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserUpdate(request.POST, instance=user_object)
        if form.is_valid():
            print(form.cleaned_data)
            print("form is valid")
            form.save()
            return redirect("/account/profile/")
        else:
            print("Form is invalid")
    elif request.method == "GET":
        form = UserUpdate(instance=user_object)
    return render(request, "app/editprofile.html", {"form":form})

@login_required(login_url="/account/login/")
def delete_profile(request):
    user_id = request.user.id
    user_object = get_object_or_404(User, id=user_id)
    user_object.delete()
    logout(request)
    return redirect("/account/login/")



def addpic(request):
    if request.method == "POST":
        file_obj = request.FILES['profilepicture']
        file_obj.name = request.user.username
        fs = FileSystemStorage()
        if fs.exists(file_obj.name):
            fs.delete(file_obj.name)
        filename = fs.save(file_obj.name, file_obj)
        return HttpResponseRedirect("/account/profile/")
    else:
        return render(request, "app/addpic.html")


class IndexView(ListView):
    template_name = "app/index.html"
    def get_queryset(self):
        return Blogging.objects.all()

    context_object_name = "data"



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')