from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'login'
urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-out/', views.sign_out, name='sign-out'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)