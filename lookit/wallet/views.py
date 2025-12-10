from django.shortcuts import render
from .models import Wallet, WalletTransactions
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, DecimalField, When, F, Value


# Create your views here.
@login_required
def wallet(request):
    # ---get wallet details, if no wallet for user create one--------
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = WalletTransactions.objects.filter(wallet=wallet).order_by(
        '-created_at'
    )
    transaction_summary = transactions.aggregate(
        total_credit=Sum(
            Case(
                When(transaction_type='credit', then=F('amount')),
                default=Value(0),
                output_field=DecimalField(),
            )
        ),
        total_debit=Sum(
            Case(
                When(transaction_type='debit', then=F('amount')),
                default=Value(0),
                output_field=DecimalField(),
            )
        )
    )

    return render(
        request,
        "wallet/wallet.html",
        {
            "wallet": wallet,
            'transactions': transactions,
            'summary': transaction_summary,
        },
    )
