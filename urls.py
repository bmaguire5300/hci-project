from django.contrib import admin
from django.urls import path
from tracker import views
from django.urls import include 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.user_login, name='login'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
