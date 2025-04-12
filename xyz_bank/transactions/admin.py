from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_type', 'sender', 'receiver', 'amount', 'status', 'created_at')
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('sender__email', 'receiver__email', 'sender__account_number', 'receiver__account_number')
    ordering = ('-created_at',)
    list_per_page = 20
