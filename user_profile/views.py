from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse


def edit_password(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            if old_password == new_password:
                return render(request, 'user_profile/edit_password.html', {'invalid_password': 'true'})
            user = User.objects.get(pk=request.user.id)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
            else:
                return render(request, 'user_profile/edit_password.html', {'invalid_password': 'true'})

        return redirect(reverse('home:home'))
    return render(request, 'user_profile/edit_password.html')


def edit_name(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form_first_name = request.POST['first_name']
            form_last_name = request.POST['last_name']
            user = User.objects.get(pk=request.user.id)
            user.first_name = form_first_name
            user.last_name = form_last_name
            user.save()

        return redirect(reverse('home:home'))
    return render(request, 'user_profile/edit_name.html')