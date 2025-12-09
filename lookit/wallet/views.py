from django.shortcuts import render
from .models import Wallet, WalletTransactions
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def wallet(request):
    wallet = Wallet.objects.get(user=request.user)
    transactions = WalletTransactions.objects.filter(wallet=wallet)
    
    return render(request, "wallet/wallet.html",{"wallet":wallet, 'transactions':transactions})