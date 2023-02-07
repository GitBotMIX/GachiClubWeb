from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'roulette'
urlpatterns = [
    path('', views.get_roulette_page, name='roulette'),
    path('to_do_quest/', views.to_do_quest, name='to_do_quest'),
    path('perform_quest/', views.perform_quest, name='perform_quest'),
    path('fail_quest/', views.fail_quest, name='fail_quest'),
    path('check_exist_completing_quest/', views.check_exist_completing_quest, name='check_exist_completing_quest'),
    path('get_quest_data/', views.get_quest_data, name='get_quest_data'),
    path('get_history_list/', views.get_history_list, name='get_history_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)