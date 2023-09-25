from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth, User
from .models import Customer, Address
from django.contrib import messages
from django.core.mail import send_mail


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
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.info(request, 'Password no matched')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email taken')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=pass1)
            user.save()
            return redirect('login')
    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def profile(request):
    if Customer.objects.filter(user=request.user).exists():
        profile = Customer.objects.get(user=request.user)
        return render(request, 'profile.html', {'profile': profile})
    else:
        profile = Customer(user=request.user)
        profile.save()
        return render(request, 'profile.html', {'profile': profile})


def updateProfile(request):
    profile = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        birthdate = request.POST['birthdate']

        if username != request.user.username:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('updateProfile')
        elif email != request.user.email:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('updateProfile')

        profile.user.username = username
        profile.user.email = email
        profile.name = name

        if birthdate:
            profile.birthdate = birthdate

        if 'profile_pic' in request.FILES:
            profile.image = request.FILES['profile_pic']

        profile.user.save()
        profile.save()
        return redirect('profile')
    else:
        return render(request, 'updateprofile.html', {'profile': profile})


def updatepass(request):
    olspass = request.POST['oldpass']
    pass1 = request.POST['pass1']
    pass2 = request.POST['pass2']

    if (pass1 != pass2 or pass1 == ''):
        messages.info(request, 'Password not matched')
        return redirect('updateProfile')
    if request.user.check_password(olspass):
        request.user.set_password(pass2)
        request.user.save()
        return redirect("/")
    else:
        messages.info(request, 'Wrong Password')
        return redirect('updateProfile')


def sendMail(request):
    send_mail(
        'ঈদ মুবারাক',
        'প্রিয় সহপাঠি,\n\nঈদুল আযহার শুভেচ্ছা গ্রহন করুন। করোনা প্যানাডেমিক এর কারনে দীর্ঘ দিন আপনার সাথে দেখা হচ্ছে না, কথা হচ্ছে না। সবাই এই আনলিমিটেড বন্ধ নামক প্যারায় অতিষ্ট হইয়ে ঊঠছে। আশা করি খুব দ্রুত পৃথীবি সুস্থ হয়ে উঠবে, আমরা আবার আমাদের ভালবাসার ক্যাম্পাসে প্রিয় ক্লাসরুমে একত্রিত হতে পারব। \n\nআপনার সুস্বাস্থ কামনা করছি, মানষিক অবসাদ এরাতে ধর্মিয় কাজ কর্মে মন দিন, বই পরুন , নিজেকে টুকটাক কাজে ব্যাস্ত রাখুন \n\nইতি,\nআপনার শুভাকাঙ্খি বন্ধু\nনয়ন।',
        'oboyob16.official@gmail.com',
        [
            'bhyean@gmail.com',
            'bhyean16@cse.pstu.ac.bd',
            # 'tonmoy16@cse.pstu.ac.bd',
            # 'taj16@cse.pstu.ac.bd',
            # 'anirban16@cse.pstu.ac.bd',
            # 'adi16@cse.pstu.ac.bd',
            # 'shifar16@cse.pstu.ac.bd',
            # 'arahman16@cse.pstu.ac.bd',
            # 'abhishek16@cse.pstu.ac.bd',
            # 'alamen15@cse.pstu.ac.bd',
            # 'alihossain16@cse.pstu.ac.bd',
            # 'amirul16@cse.pstu.ac.bd',
            # 'anik16@cse.pstu.ac.bd',
            # 'arjon16@cse.pstu.ac.bd',
            # 'ayshea16@cse.pstu.ac.bd',
            # 'fariha16@cse.pstu.ac.bd',
            # 'farzanaakter16@cse.pstu.ac.bd',
            # 'oni16@cse.pstu.ac.bd',
            # 'sajib16@cse.pstu.ac.bd',
            # 'imad16@cse.pstu.ac.bd',
            # 'hasan16@cse.pstu.ac.bd',
            # 'jahid16@cse.pstu.ac.bd',
            # 'shapla16@cse.pstu.ac.bd',
            # 'lamia16@cse.pstu.ac.bd',
            # 'mahfuz16@cse.pstu.ac.bd',
            # 'orna16@cse.pstu.ac.bd',
            # 'adnan16@cse.pstu.ac.bd',
            # 'mithil16@cse.pstu.ac.bd',
            # 'shefat16@cse.pstu.ac.bd',
            # 'tahsin16@cse.pstu.ac.bd',
            # 'rakib16@cse.pstu.ac.bd',
            # 'jamiul16@cse.pstu.ac.bd',
            # 'rakibul16@cse.pstu.ac.bd',
            # 'rony16@cse.pstu.ac.bd',
            # 'miran16@cse.pstu.ac.bd',
            # 'shahriar16@cse.pstu.ac.bd',
            # 'mehedihasan16@cse.pstu.ac.bd',
            # 'almuzahid16@cse.pstu.ac.bd',
            # 'nazmul16@cse.pstu.ac.bd',
            # 'partha16@cse.pstu.ac.bd',
            # 'sejan16@cse.pstu.ac.bd',
            # 'ruhitshah16@cse.pstu.ac.bd',
            # 'sabbirmim16@cse.pstu.ac.bd',
            # 'skrakib16@cse.pstu.ac.bd',
            # 'shishir16@cse.pstu.ac.bd',
            # 'shyamsaikat16@cse.pstu.ac.bd',
            # 'sifat16@cse.pstu.ac.bd',
            # 'sourav16@cse.pstu.ac.bd',
            # 'tahmid16@cse.pstu.ac.bd',
            # 'sonaly16@cse.pstu.ac.bd',
            # 'tasnif16@cse.pstu.ac.bd',
        ],
        fail_silently=False,
    )

    return redirect('/')


def addressBook(request):
    addresses = Address.objects.filter(customer__user=request.user)
    return render(request, 'address.html', {'addresses': addresses})


def showAddress(request, id):
    address = Address.objects.get(id=id)
    return render(request, 'address_edit.html', {'address': address})


def addAddress(request):
    customer = Customer.objects.get(user=request.user)
    address = Address()
    address.customer = customer
    address.address_name = request.POST['address_name']
    address.mobile = request.POST['mobile']
    address.alternate_mobile = request.POST['alternate_mobile']
    address.division = request.POST['division']
    address.district = request.POST['district']
    address.upazila = request.POST['upazila']
    address.zipcode = request.POST['zipcode']
    address.address = request.POST['address']
    address.save()
    return redirect('address')


def editAddress(request):
    id = request.POST['id']

    address = Address.objects.get(id=id)

    address.address_name = request.POST['address_name']
    address.mobile = request.POST['mobile']
    address.alternate_mobile = request.POST['alternate_mobile']
    address.division = request.POST['division']
    address.district = request.POST['district']
    address.upazila = request.POST['upazila']
    address.zipcode = request.POST['zipcode']
    address.address = request.POST['address']
    address.save()

    return redirect('address')


def deleteAddress(request, id):
    address = Address.objects.get(id=id)
    address.delete()
    return redirect('address')