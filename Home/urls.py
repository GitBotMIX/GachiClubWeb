from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.get_home_page, name='home'),
    path('perform_task/', views.perform_task, name='perform_task'),
    path('delete_task/', views.delete_task, name='delete_task'),
    path('get_rating/', views.get_rating, name='get_rating'),
    path('completed_tasks/', views.completed_tasks, name='completed_tasks'),
    path('get_user_punishment/', views.get_user_punishment, name='get_user_punishment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)