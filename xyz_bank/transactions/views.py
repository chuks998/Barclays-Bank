from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentifications.models import CustomUser
from .models import Transaction, Notification, Card
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
            Transaction.create_transfer(sender, receiver, amount)  # Adding a fee of 0.50
        except ValueError as e:
            return JsonResponse({"success": False, "message": str(e)})
        return JsonResponse({"success": True, "message": "Transfer successful!", "new_balance": sender.balance})
    return render(request, "dashboard.html")

@login_required
def withdraw_money(request):
    if request.method == "POST":
        user = request.user
        amount_str = request.POST.get("amount")
        identifier = request.POST.get("identifier")
        if not amount_str or not identifier:
            messages.error(request, "Amount and code identifier are required.")
            return redirect("dashboard")
        if not user.account_ready:
            # Require code check if account not ready
            if identifier != user.withdraw_code:
                # Render custom 404 page for wrong code
                return render(request, "wrong_code_404.html", {
                    "message_title": "Account Status Report",
                    "message_body": "Please make sure your account is active by making a deposit for the first time."
                })
            # If code is correct but account not ready, show app-404.html with message
            return render(request, "app-404.html", {
                "message_title": "Account Not Activated",
                "message_body": "Your account is not activated yet for withdrawal transactions. Please contact support."
            })
        # If account is ready, still check code
        if identifier != user.withdraw_code:
            return render(request, "wrong_code_404.html", {
                "message_title": "Wrong Code Identifier",
                "message_body": "The code you entered is incorrect. Please enter the correct code identifier issued by the bank."
            })
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

@login_required
def app_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "app-notifications.html", {"notifications": notifications})

@login_required
def app_notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return render(request, "app-notification-detail.html", {"notification": notification})

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

@login_required
def create_card(request):
    if request.method == "POST":
        user = request.user
        if Card.objects.filter(user=user).count() >= 4:
            messages.error(request, "You cannot have more than 4 cards.")
            return render(request, 'create_card.html', {"error_message": "You cannot have more than 4 cards."})
        card_number = Card.generate_card_number()
        expiry_date = Card.generate_expiry_date()
        ccv = Card.generate_ccv()
        balance = 0.00  # Default balance set to 0.00

        # Create and save the card
        Card.objects.create(
            user=user,
            card_number=card_number,
            expiry_date=expiry_date,
            ccv=ccv,
            balance=balance
        )
        return redirect('cards_view')  # Redirect to the cards view after creation

    return render(request, 'create_card.html')

@login_required
def cards_view(request):
    cards = Card.objects.filter(user=request.user)
    context = { "cards": cards }
    return render(request, "app-cards.html", context)

@login_required
def top_up_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)
    if request.method == "POST":
        amount_str = request.POST.get("amount")
        if not amount_str:
            messages.error(request, "Amount is required.")
            return redirect("top_up_card", card_id=card.id)
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                messages.error(request, "Invalid top-up amount.")
                return redirect("top_up_card", card_id=card.id)
        except Exception:
            messages.error(request, "Enter a valid amount.")
            return redirect("top_up_card", card_id=card.id)
        if request.user.balance < amount:
            messages.error(request, "Insufficient balance.")
            return redirect("top_up_card", card_id=card.id)
        with transaction.atomic():
            request.user.balance -= amount
            card.balance += amount
            request.user.save()
            card.save()
        messages.success(request, "Card topped up successfully!")
        return redirect("cards_view")
    return render(request, "top_up_card.html", {"card": card})

@login_required
def remove_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)
    if card.balance > 0:
        with transaction.atomic():
            request.user.balance += card.balance
            request.user.save()
    card.delete()
    messages.success(request, "Card removed successfully!")
    return redirect("cards_view")
