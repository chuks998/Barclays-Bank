from django.db import models, transaction as db_transaction
from authentifications.models import CustomUser
from django.contrib.auth import get_user_model
import random
from datetime import datetime, timedelta

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("Transfer", "Transfer"),
        ("Withdrawal", "Withdrawal"),
    ]
    
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]
    
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_transactions", null=True, blank=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_transactions", null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_transfer(cls, sender, receiver, amount):
        with db_transaction.atomic():
            if sender.balance >= amount:
                sender.balance -= amount
                receiver.balance += amount
                sender.save()
                receiver.save()
                transaction = cls.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    transaction_type="Transfer",
                    status="Completed"
                )
                # Create a notification for the receiver
                Notification.create_notification(
                    user=receiver,
                    message=f"You have received ${amount} from {sender.username}."
                )
            else:
                transaction = None  # Assign None if the condition fails
                raise ValueError("Insufficient balance.")
        return transaction

    @classmethod
    def create_withdrawal(cls, sender, amount):
        with db_transaction.atomic():
            if sender.balance >= amount:
                sender.balance -= amount
                sender.save()
                return cls.objects.create(
                    sender=sender,
                    amount=amount,
                    transaction_type="Withdrawal",
                    status="Completed"
                )
            else:
                raise ValueError("Insufficient funds for withdrawal.")

    def __str__(self):
        if self.transaction_type == "Transfer":
            return f"Transfer: {self.sender.name} -> {self.receiver.name} (${self.amount})"
        return f"Withdrawal: {self.sender.name} (${self.amount})"

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_notification(user, message):
        """Create a notification for a specific user."""
        Notification.objects.create(user=user, message=message)

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.is_read else 'Unread'}"

class Card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cards")
    card_number = models.CharField(max_length=16, unique=True)
    expiry_date = models.DateField()
    ccv = models.CharField(max_length=3)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.card_number}"

    @staticmethod
    def generate_card_number():
        return ''.join([str(random.randint(0, 9)) for _ in range(16)])

    @staticmethod
    def generate_expiry_date():
        return datetime.now().date() + timedelta(days=365 * 3)  # 3 years from now

    @staticmethod
    def generate_ccv():
        return ''.join([str(random.randint(0, 9)) for _ in range(3)])

    @property
    def last_four_digits(self):
        return self.card_number[-4:]
