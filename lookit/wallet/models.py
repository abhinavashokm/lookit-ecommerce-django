from django.db import models
from user.models import User

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=2, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class WalletTransactions(models.Model):
    
    class TransactionType(models.Choices):
        CREDIT = 'credit'
        DEBIT = 'debit'
        
    class TransactionSource(models.Choices):
        REWARD = 'reward'
        ONLINE = 'online'
        SHOPPING = 'shopping'
        REFUND = 'refund'
        
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=2, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices) #credit or debit
    label = models.CharField(max_length=100) 
    txn_source = models.CharField(max_length=100, choices=TransactionType.choices)  #from where the money came or where it gone
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
