from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import User

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)

                return redirect(reverse('dashboard'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            messages.warning(request, 'Incorrect Details, Try Again!')
            return redirect(reverse('login'))
    else:
        return render(request, 'login.html')


def dashboard(request):
    context_dict = {}

    return render(request, 'dashboard.html', context=context_dict)


def profile(request):
    user = User.objects.get(id=request.user.id)
    context_dict = {}
    context_dict['diet'] = user.meat_mult

    return render(request, 'profile.html', context=context_dict)


def challenge(request):
    context_dict = {}

    return render(request, 'challenge.html', context=context_dict)


def submit_challenge(request):

    if request.method == 'POST':
        meat = request.POST.get('meat', '')
        print(meat)

    return render(request, 'challenge.html')

def update_profile(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.meat_mult = request.POST.get('diet', '')
        user.car_mult = request.POST.get('car', '')
        user.save()
        print(user.meat_mult)
        print(user.car_mult)

    user = User.objects.get(id=request.user.id)
    context_dict = {}
    context_dict['diet'] = user.meat_mult    
    return render(request, 'profile.html', context=context_dict)        