from django.urls import path
from .views import (
    settings, error_404_view,
    change_profile_picture, change_password, change_email, change_username
)

urlpatterns = [
    path('dashboard/settings', settings, name='settings'),
    path('dashboard/change-profile-picture', change_profile_picture, name='change_profile_picture'),
    path('dashboard/change-password', change_password, name='change_password'),
    path('dashboard/change-email', change_email, name='change_email'),
    path('dashboard/change-username', change_username, name='change_username'),
]