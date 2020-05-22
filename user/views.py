from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
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
        elif User.objects.filter(email=email).exists():
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
    print(request.user.username)
    auth.logout(request)
    return redirect('/')

def profile(request):
    return render(request,'profile.html')

def product(request):
    print()
    return render(request,'product.html')
