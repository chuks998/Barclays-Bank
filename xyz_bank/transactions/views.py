from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentifications.models import CustomUser
from .models import Transaction, Notification
from django.db import transaction
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def transfer_money(request):
    if request.method == "POST":
        sender = request.user  
        receiver_account = request.POST.get("receiver_account")
        amount_str = request.POST.get("amount")
        password = request.POST.get("password")
        if not receiver_account or not amount_str or not password:
            return JsonResponse({"success": False, "message": "All fields are required."})
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                return JsonResponse({"success": False, "message": "Invalid transfer amount."})
        except Exception:
            return JsonResponse({"success": False, "message": "Enter a valid amount."})
        if not sender.check_password(password):
            return JsonResponse({"success": False, "message": "Incorrect password."})
        try:
            receiver = CustomUser.objects.get(account_number=receiver_account)
        except CustomUser.DoesNotExist:
            return JsonResponse({"success": False, "message": "Receiver account not found."})
        try:
            Transaction.create_transfer(sender, receiver, amount)
        except ValueError as e:
            return JsonResponse({"success": False, "message": str(e)})
        return JsonResponse({"success": True, "message": "Transfer successful!", "new_balance": sender.balance})
    return render(request, "dashboard.html")

@login_required
def withdraw_money(request):
    if request.method == "POST":
        user = request.user
        if not user.account_ready:  # Check if account is ready for withdrawal
            return render(request, "error.html", {"message": "You cannot withdraw until you have made at least one deposit."})
        amount_str = request.POST.get("amount")
        if not amount_str:
            messages.error(request, "Amount is required.")
            return redirect("dashboard")
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                messages.error(request, "Invalid withdrawal amount.")
                return redirect("dashboard")
        except Exception:
            messages.error(request, "Enter a valid amount.")
            return redirect("dashboard")
        try:
            Transaction.create_withdrawal(user, amount)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("dashboard")
        messages.success(request, "Withdrawal successful!")
        return redirect("dashboard")
    return redirect("dashboard")

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(receiver=request.user)
    transactions = transactions.order_by("-created_at")
    return render(request, "app-transactions.html", {"transactions": transactions})

@login_required
def transaction_details(request, pk):
    transaction_obj = get_object_or_404(Transaction, pk=pk)
    if not (transaction_obj.sender == request.user or transaction_obj.receiver == request.user):
        messages.error(request, "You are not authorized to view this transaction.")
        return redirect("transaction_history")
    return render(request, "app-transaction-detail.html", {"transaction": transaction_obj})

def get_notifications(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    data = {
        "notifications": list(notifications.values("id", "message", "is_read", "created_at")),
        "unread_count": unread_count
    }
    return JsonResponse(data)

@csrf_exempt
def mark_notifications_read(request):
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({"message": "All notifications marked as read."})
    return JsonResponse({"error": "User not authenticated"}, status=401)

@login_required
def deposit_bank_transfer(request):
    # Dummy view for bank transfer deposit; replace with proper implementation.
    return render(request, "deposit_bank_transfer.html")

@login_required
def deposit_gift_card(request):
    # Dummy view for gift card deposit; replace with proper implementation.
    return render(request, "deposit_gift_card.html")
