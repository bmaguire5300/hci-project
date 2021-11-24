from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from django.db.models import Sum
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
    groups = Group.objects.all()
    context_dict['diet'] = user.meat_mult
    context_dict['car'] = user.car_mult  
    context_dict['water'] = user.water_mult
    context_dict['foodsource'] = user.foodsource_mult
    context_dict['groups'] = groups
    context_dict['user_group'] = user.group.id



    return render(request, 'profile.html', context=context_dict)


def challenge(request):
    context_dict = {}

    return render(request, 'challenge.html', context=context_dict)


def submit_challenge(request):

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        meat = user.meat_mult * int(request.POST.get('meat', '0'))
        bike = user.car_mult * int(request.POST.get('bike', '0'))
        train = user.car_mult * int(request.POST.get('train', '0'))
        bus = user.car_mult * int(request.POST.get('bus', '0'))
        shower = user.water_mult * int(request.POST.get('shower', '0'))
        organic = user.foodsource_mult * int(request.POST.get('organic', '0'))

        total = sum([meat, bike, train, bus, shower, organic])
        completed = CompletedChallenge.objects.create(user=user, total_points=total)

    return redirect('leaderboard')

def update_profile(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.meat_mult = request.POST.get('diet', '')
        user.car_mult = request.POST.get('car', '')
        user.water_mult = request.POST.get('water', '')
        user.foodsource_mult = request.POST.get('foodsource', '')
        user.group = Group.objects.get(id=(request.POST.get('group', '')))
        print(user.group)
        user.save()
     
    return profile(request)        


def leaderboard(request):
    context_dict = {}

    results = CompletedChallenge.objects.values('user__group__name') \
            .annotate(result_total= Sum('total_points')) \
            .order_by('-result_total')

    context_dict['results'] = results
    print(context_dict['results'])


    return render(request, 'leaderboard.html', context=context_dict)