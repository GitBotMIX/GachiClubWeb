from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'user_profile'
urlpatterns = [
    path('edit/password', views.edit_password, name='edit_password'),
    path('edit/name', views.edit_name, name='edit_name'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)