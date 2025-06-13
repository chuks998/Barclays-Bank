app_name = "dashboard_func"

from django.urls import path
from .views import (
    transfer_money, withdraw_money, get_notifications, mark_notifications_read,
    transaction_history, transaction_details, top_up_card, remove_card,
    app_notifications, app_notification_detail
)

urlpatterns = [
    path('transfer/', transfer_money, name='transfer_money'),
    path('withdraw/', withdraw_money, name='withdraw'),
    path('notifications/', get_notifications, name='get_notifications'),
    path('mark-notifications-read/', mark_notifications_read, name='mark_notifications_read'),
    path('history/', transaction_history, name='transaction_history'),
    path('detail/<int:pk>/', transaction_details, name='transaction_detail'),
    path('cards/top-up/<int:card_id>/', top_up_card, name='top_up_card'),
    path('cards/remove/<int:card_id>/', remove_card, name='remove_card'),
    path('app-notifications/', app_notifications, name='app_notifications'),
    path('app-notification-detail/<int:notification_id>/', app_notification_detail, name='app_notification_detail'),
]
