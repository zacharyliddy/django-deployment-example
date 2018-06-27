from django.shortcuts import render
from UserApp.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.
def index(request):
    return render(request,'UserApp/index.html')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            #one to one relationship
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'UserApp/registration.html',
                            {'user_form':user_form,
                             'profile_form':profile_form,
                              'registered':registered})
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpRepsonse("You are logged in, Nice!")


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpRepsonse("Account not active")

        else:
            print("Someone tried to login and failed!")
            print(f("Username: {username} and password {password}"))
            return HttpRepsonse("Invalid login details supplied!")
    else:
        return render(request,'UserApp/login.html', {})
