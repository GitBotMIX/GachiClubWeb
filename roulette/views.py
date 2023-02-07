from django.core import serializers
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from urllib.parse import parse_qs
from Home.models import Gifts
import roulette
from roulette.models import RouletteItems, RouletteHistory, RouletteUserProfile


def get_user_profile_quest_data(roulette_user_profile):
    return {'quest_is_exist': True,
                             'quest_in_progress__title': roulette_user_profile.quest_in_progress.get_title(),
                             'quest_in_progress__description': roulette_user_profile.quest_in_progress.get_description(),
                             'quest_in_progress__reward': roulette_user_profile.quest_in_progress.get_reward(),
                             'quest_in_progress__id': roulette_user_profile.quest_in_progress.id}


def check_exist_completing_quest(request):
    quest_is_exist = False
    roulette_user_profile = RouletteUserProfile.objects.get(user=request.user)
    if roulette_user_profile.quest_in_progress:
        quest_is_exist = True
    if request.method == 'POST':
        if quest_is_exist:
            return JsonResponse(get_user_profile_quest_data(roulette_user_profile))
        else:
            return JsonResponse({'quest_is_exist': False})
    return quest_is_exist


def get_roulette_page(request):
    roulette_items = RouletteItems.objects.all()
    roulette_history = RouletteHistory.objects.filter(user=request.user).order_by('-completed_at')
    gifts = Gifts.objects.all()
    gift = None
    if gifts:
        gift = gifts[0]
    try:
        roulette_user_profile = RouletteUserProfile.objects.get(user=request.user)
    except roulette.models.RouletteUserProfile.DoesNotExist:
        roulette_user_profile = RouletteUserProfile(user=request.user)
        roulette_user_profile.save()

    return render(request, 'roulette/index.html', {'roulette_items': roulette_items,
                                                   'roulette_items_len': RouletteItems.length(),
                                                   'roulette_history': roulette_history[0:12],
                                                   'roulette_history_len': len(roulette_history),
                                                   'roulette_user_profile': roulette_user_profile,
                                                   'gift': gift})


def to_do_quest(request):
    data = parse_qs(str(request.body.decode('utf-8')))
    roulette_total_spin = RouletteUserProfile.objects.add_spin(request.user)
    quest = RouletteItems.objects.get(pk=data['item_id'][0])
    roulette_user_profile = RouletteUserProfile.objects.get(user=request.user)
    if roulette_user_profile.quest_in_progress:
        return JsonResponse(get_user_profile_quest_data(roulette_user_profile))
    roulette_user_profile.quest_in_progress = quest
    roulette_user_profile.save()
    RouletteHistory(user=request.user, completed_quest=quest, is_completed_quest=False).save()
    return JsonResponse({'roulette_total_spin': roulette_total_spin})


def perform_quest(request):
    data = parse_qs(str(request.body.decode('utf-8')))
    user_profile = RouletteUserProfile.objects.get(user=request.user)
    current_not_completed_quest = user_profile.quest_in_progress
    RouletteUserProfile.objects.add_completed_quest(request.user, current_not_completed_quest,
                                                    user_profile=user_profile)
    return JsonResponse({'success': True})


def fail_quest(request):
    data = parse_qs(str(request.body.decode('utf-8')))
    user_profile = RouletteUserProfile.objects.get(user=request.user)
    current_not_completed_quest = user_profile.quest_in_progress
    RouletteUserProfile.objects.add_not_completed_quest(request.user,current_not_completed_quest,
                                                        user_profile=user_profile)
    return JsonResponse({'success': True})


def get_quest_data(request):
    data = parse_qs(str(request.body.decode('utf-8')))
    print(data['item_id'][0])
    quest = RouletteItems.objects.get(pk=data['item_id'][0])
    return JsonResponse({'quest__title': quest.get_title(),
                         'quest__description': quest.get_description(),
                         'quest__reward': quest.get_reward(),
                         'quest__id': quest.id
                         })


def get_history_list(request):
    if request.method == 'POST':
        user_history = RouletteHistory.objects.filter(user=request.user).order_by('-completed_at')
        user_profile = RouletteUserProfile.objects.get(user=request.user)
        quest_in_progress = user_profile.quest_in_progress
        data = []
        for count, item in enumerate(user_history):
            is_current_completing_quest = False
            if count == 0 and quest_in_progress == item.completed_quest:
                is_current_completing_quest = True
            data.append({
                "completed_quest__id": item.completed_quest.id,
                "completed_quest__title": item.completed_quest.get_title(),
                "is_completed_quest": item.is_completed_quest,
                "is_current_completing_quest" : is_current_completing_quest,
            })
        return JsonResponse({'roulette_history': data[:12],
                             'user_profile_data': {'total_quest_completed': user_profile.total_completed_quest,
                                                   'total_quest_not_completed': user_profile.total_not_completed_quest,
                                                   'total_spin': user_profile.total_spin}})
    else:
        return get_roulette_page(request)
