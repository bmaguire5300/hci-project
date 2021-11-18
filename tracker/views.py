from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

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