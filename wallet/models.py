from django.db import models
from django.contrib.auth.models import User
import uuid

class UserWallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s wallet"


class Transaction(models.Model):
    FUND = 'D'
    WITHDRAWAL = 'W'
    TRANSFER = 'T'

    TRANSACTION_TYPES = [
        (FUND, 'Fund'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} of {self.amount} in {self.wallet.user.username}'s wallet"
    
# class Transfer(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     sender = models.ForeignKey(User, related_name='transfers_sent', on_delete=models.CASCADE)
#     recipient = models.ForeignKey(User, related_name='transfers_received', on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"Transfer from {self.sender.username} to {self.recipient.username} of R {self.amount}"

class logs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userwallet= models.ForeignKey(UserWallet, on_delete=models.CASCADE, related_name='logs')
    amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
            return f"{self.userwallet.user.username}'s log"