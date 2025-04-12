from django.urls import path
from .views import register, user_login, password_reset_request,set_language, set_currency, dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('', user_login, name='user_login'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path("set-language/", set_language, name="set_language"),
    path("set-currency/", set_currency, name="set_currency"),
    path("dashboard/", dashboard, name="dashboard"),
]

    # path('activate/<uidb64>/<token>/', activate_account, name='activate'),
