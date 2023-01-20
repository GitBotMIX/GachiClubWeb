from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Gifts, Quests, Category, UserQuests, UserProfile
from django.utils import timezone
from urllib.parse import parse_qs
from django.contrib.auth.models import User
from django.db.models import Max, Count
from django.db.models import Q
import json


def get_home_page(request):
    if request.user.is_authenticated:
        gifts = Gifts.objects.all()
        quests = Quests.objects.filter(available=True)
        categories = Category.objects.all()
        show_gift = None
        gift = None
        user_quests = UserQuests.objects.filter(user=request.user)
        for quest in quests:
            quest.user_completion = UserQuests.objects.filter(quest_completed=quest, user=request.user).count()

        if gifts:
            gift = gifts[0]
        return render(request, 'Home/index.html', {'user': request.user, 'gift': gift,
                                                   'quests': quests, 'categories': categories,
                                                   'user_quests': user_quests})
    else:
        return redirect(reverse('login:sign-up'))


def perform_task(request):
    if request.method == 'POST':
        data = parse_qs(str(request.body.decode('utf-8')))
        user = User.objects.get(pk=data['user_id'][0])
        quest = Quests.objects.get(pk=data['quest_id'][0])
        points = data['points'][0]

        user_quests = UserQuests.objects.filter(user=user, quest_completed=quest)
        try:
            if len(user_quests) >= user_quests[0].quest_completed.amount_available_user:
                return JsonResponse({'error': 'Invalid request method'})
        except IndexError:
            pass
        UserQuests(user=user, quest_completed=quest).save()
        UserProfile.objects.add_points(user, points)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def get_rating(request):
    if request.method == 'POST':
        users_rating = UserProfile.objects.get_ranking()
        return JsonResponse({'response': list(users_rating.values('user__first_name', 'user__last_name', 'points'))})