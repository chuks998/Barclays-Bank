from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from transactions.models import Card  # Import the Card model

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "name", "username", "country", "account_number", "balance", "withdraw_code", "is_active", "is_staff", "date_joined", "account_ready")
    list_filter = ("is_active", "is_staff", "country")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "username", "country", "profile_picture")}),
        ("Account Details", {"fields": ("account_number", "balance", "withdraw_code", "date_joined", "account_ready")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "username", "country", "password1", "password2", "profile_picture"),
        }),
    )
    search_fields = ("email", "username", "name")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")

class CardAdmin(admin.ModelAdmin):
    list_display = ("user", "card_number", "expiry_date", "ccv", "balance")
    search_fields = ("user__username", "card_number")
    list_filter = ("expiry_date",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Card, CardAdmin)  # Register the Card model with the admin
