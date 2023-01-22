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


def task_manipulator(request, delete_task=False):

    data = parse_qs(str(request.body.decode('utf-8')))
    user = User.objects.get(pk=data['user_id'][0])
    quest = Quests.objects.get(pk=data['quest_id'][0])
    points = data['points'][0]

    if delete_task:
        UserQuests.objects.filter(user=user, quest_completed=quest)[0].delete()
        UserProfile.objects.remove_points(user, points)
    else:
        UserQuests(user=user, quest_completed=quest).save()
        UserProfile.objects.add_points(user, points)
    return JsonResponse({'error': 'Invalid request method'})


def perform_task(request):
    if request.method == 'POST':
        task_manipulator(request)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def delete_task(request):
    if request.method == 'POST':

        task_manipulator(request, delete_task=True)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def get_rating(request):
    if request.method == 'POST':
        users_rating = UserProfile.objects.get_ranking()
        return JsonResponse({'response': list(users_rating.values('user__first_name', 'user__last_name', 'points'))})


def completed_tasks(request):
    if request.method == 'POST':
        pass
    else:
        if request.user.is_authenticated:
            user_quests = UserQuests.objects.filter(user=request.user)
            added_quests = []
            # user_quests = UserQuests.objects.filter(user=request.user, quest_completed=True).annotate(
            #     user_completion=Count('user'))

            # for user_quest in user_quests:
            #     print(user_quest.user_completion)
            for user_quest in user_quests:

                if user_quest.quest_completed.id not in added_quests:
                    print(user_quest.quest_completed.id)
                    user_quest.user_completion = user_quests.filter(quest_completed=user_quest.quest_completed,
                                                                           user=request.user).count()
                    added_quests.append(user_quest.quest_completed.id)
            return render(request, 'Home/completed_tasks.html', {'user_quests': user_quests})

