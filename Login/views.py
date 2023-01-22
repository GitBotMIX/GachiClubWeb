from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from Home.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse


def sign_out(request):
    logout(request)
    return redirect(reverse('login:sign-up'))


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            #return redirect(reverse('home:home'))
            return redirect(reverse('home:home'))
        else:
            return render(request, 'Login/sign-in/index.html', {'incorrect_input': 'true'})
    else:
        if request.user.is_authenticated:
            logout(request)
            return render(request, 'Login/sign-in/index.html')
        else:
            return render(request, 'Login/sign-in/index.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect(reverse('home:home'))

    if request.method == 'POST':
        user_name = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        try:
            user = User.objects.create_user(user_name, password=password, first_name=first_name, last_name=last_name)
        except IntegrityError:
            return render(request, 'Login/sign-up/index.html', {'incorrect_input': 'true'})
        login(request, user)
        UserProfile(user=user).save()
        return redirect(reverse('home:home'))
    return render(request, 'Login/sign-up/index.html')


def sign_up_qr_code(request, first_name, last_name, username, password):
    if request.user.is_authenticated:
        return redirect(reverse('home:home'))
    try:
        user = User.objects.create_user(username, password=password, first_name=first_name, last_name=last_name)
    except IntegrityError:
        return render(request, 'Login/sign-up/index.html')
    login(request, user)
    UserProfile(user=user).save()
    return redirect(reverse('home:home'))