from django.db import models
from django.contrib.auth.hashers import make_password
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # override the save method to ensure that the password is hashed before save, while passing the args and kwargs to ensure these variables are still passed to the super class. THis way, the save method does not loose its functionality
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs) 
    def __str__(self):
        return self.username

class UserWallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # overriding the default implementation of this special method 
    def __str__(self):
        return f"{self.user.username}'s wallet"
    
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