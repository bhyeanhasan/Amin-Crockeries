from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages


# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.info(request,'Password no matched')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email taken')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=pass1, first_name=first_name,last_name=last_name)
            user.save()
            print('user done')


        return redirect('/')

    else:
        return render(request, 'register.html');
