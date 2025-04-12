from django.db import models, transaction
from authentifications.models import CustomUser
from django.contrib.auth import get_user_model

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
        with transaction.atomic():
            if sender.balance >= amount:
                sender.balance -= amount
                receiver.balance += amount
                sender.save()
                receiver.save()
                return cls.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    transaction_type="Transfer",
                    status="Completed"
                )
            else:
                raise ValueError("Insufficient funds for transfer.")

    @classmethod
    def create_withdrawal(cls, sender, amount):
        with transaction.atomic():
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

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.is_read else 'Unread'}"
