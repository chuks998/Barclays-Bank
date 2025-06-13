from django.contrib import admin
from .models import Transaction
# from .views import send_notification  # Assuming send_notification exists in .views

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_type', 'sender', 'receiver', 'amount', 'status', 'created_at')
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('sender__email', 'receiver__email', 'sender__account_number', 'receiver__account_number')
    ordering = ('-created_at',)
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            self.notify_admin(f"Transaction {obj.id} has been updated.")
        else:
            self.notify_admin(f"Transaction {obj.id} has been created.")

    def notify_admin(self, message):
        # Use the send_notification logic from .views
        print(self.message)
