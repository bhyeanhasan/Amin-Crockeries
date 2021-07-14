from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from .models import Profile
from django.contrib import messages


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'User not found')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.info(request, 'Password no matched')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email taken')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=pass1, first_name=first_name,
                                            last_name=last_name)
            user.save()
            return redirect('login')

    else:
        return render(request, 'register.html');


def logout(request):
    auth.logout(request)
    return redirect('/')


def profile(request):

    profile = Profile.objects.filter(user=request.user)

    return render(request, 'profile.html',{'profile':profile})


def product(request):
    return render(request, 'product.html')


def updateprofile(request):
    return render(request, 'updateprofile.html')


def updateUser(request):
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']

    if request.user.username != username:
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken')
            return redirect('updateprofile')
    if request.user.email != email:
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email taken')
            return redirect('updateprofile')

    request.user.username = username
    request.user.first_name = first_name
    request.user.last_name = last_name
    request.user.email = email
    request.user.save()
    return redirect('profile')

def updatepass(request):
    olspass = request.POST['oldpass']
    pass1 = request.POST['pass1']
    pass2 = request.POST['pass2']

    if(pass1 != pass2 or pass1==''):
        messages.info(request, 'Password not matched')
        return redirect('updateprofile')
    if request.user.check_password(olspass):
        request.user.set_password(pass2)
        request.user.save()
        return redirect("/")
    else:
        messages.info(request, 'Wrong Password')
        return redirect('updateprofile')
