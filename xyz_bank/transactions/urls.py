app_name = "dashboard_func"

from django.urls import path
from .views import transfer_money, withdraw_money, get_notifications, mark_notifications_read, transaction_history, transaction_details

urlpatterns = [
    path('transfer/', transfer_money, name='transfer_money'),
    path('withdraw/', withdraw_money, name='withdraw'),
    path('notifications/', get_notifications, name='notifications'),
    path('mark-notifications-read/', mark_notifications_read, name='mark_notifications_read'),
    path('history/', transaction_history, name='transaction_history'),
    path('detail/<int:pk>/', transaction_details, name='transaction_detail'),
]
