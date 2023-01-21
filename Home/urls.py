from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.get_home_page, name='home'),
    path('perform_task/', views.perform_task, name='perform_task'),
    path('get_rating/', views.get_rating, name='get_rating'),
    path('completed_tasks/', views.completed_tasks, name='completed_tasks'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)