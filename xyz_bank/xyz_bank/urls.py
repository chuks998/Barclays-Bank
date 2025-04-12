from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from transactions.views import (transfer_money, withdraw_money, transaction_history, transaction_details,
                                  get_notifications, mark_notifications_read, deposit_bank_transfer, deposit_gift_card)
from basic.views import settings as basic_settings  # <-- new import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentifications.urls')),
    path('transactions/transfer/', transfer_money, name='transfer_money'),
    path('transactions/withdraw/', withdraw_money, name='withdraw_money'),
    path('transactions/history/', transaction_history, name='transaction_history'),
    path('transactions/<int:pk>/', transaction_details, name='transaction_detail'),
    path('notifications/', get_notifications, name='notifications'),
    path('notifications/mark-read/', mark_notifications_read, name='mark_notifications_read'),
    path('dashboard/settings/', basic_settings, name='settings'),
    path('deposit/bank-transfer/', deposit_bank_transfer, name='bank_transfer_deposit'),
    path('deposit/gift-card/', deposit_gift_card, name='deposit_gift_card'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
