from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from transactions.views import (deposit_bank_transfer, deposit_gift_card, create_card, cards_view)
from basic.views import settings as basic_settings
from basic.views import error_404_view
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentifications.urls')),
    path('settings/', include('basic.urls')),
    path('transactions/', include('transactions.urls', namespace='dashboard_func')),  # Ensure namespace is correct
    path('dashboard/settings/', basic_settings, name='settings'),
    path('dashboard/error-404', error_404_view, name='error_404_view'),
    path('deposit/bank-transfer/', deposit_bank_transfer, name='bank_transfer_deposit'),
    path('deposit/gift-card/', deposit_gift_card, name='deposit_gift_card'),
    path('create-card/', create_card, name='create_card'),
    path('cards/', cards_view, name='cards_view'),
    path('support/', include('user_support.urls')),
    path("wrong_code_404/", TemplateView.as_view(template_name="wrong_code_404.html"), name="wrong_code_404"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
