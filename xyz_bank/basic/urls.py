from django.urls import path
from .views import settings

urlpatterns = [
    path('dashboard/settings', settings, name='settings'),
]