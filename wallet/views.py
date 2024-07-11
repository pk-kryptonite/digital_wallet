from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserWallet, Transaction
from .forms import FundForm, TransferForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@login_required
def wallet(request):
    if request.method == 'GET':
        user = request.user
       
        user_wallets = UserWallet.objects.filter(user=user)
        paginator = Paginator(Transaction.objects.filter(wallet__user=user).order_by('-created_at'), 5)  # Show 10 transactions per page
        page = request.GET.get('page')
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            transactions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            transactions = paginator.page(paginator.num_pages)
        context = {
                'user': user.username,
                'user_wallets': user_wallets,
                "user_auth": user.is_authenticated,
                "transaction": transactions
            }
        
        return render(request, 'wallet.html', context)

@login_required
def fund_wallet(request):
    if request.method == 'POST':
        form = FundForm(request.POST)
        if form.is_valid():
            try:
                amount = form.cleaned_data['amount']
                wallet_id = form.cleaned_data['wallet_id']
                user_wallet = get_object_or_404(UserWallet, id=wallet_id, user=request.user)
                user_wallet.amount += amount
                user_wallet.save()
                Transaction.objects.create(
    wallet=user_wallet,
    transaction_type=Transaction.FUND,
    amount=amount,
    description=""
)
                messages.success(request, f'Wallet was successfully funded with R {amount}')
                return redirect('wallet')
            except Exception as e:
                messages.error(request, f'There was an error when funding wallet with R {amount}')
                return redirect('wallet')
        else:
            messages.error(request, "The input is invalid in form")
    return redirect('wallet')

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            try:
                amount = form.cleaned_data['amount']
                wallet_id = form.cleaned_data['wallet_id']
                user_wallet = get_object_or_404(UserWallet, id=wallet_id, user=request.user)
                if amount <= user_wallet.amount:
                    recipient_username = form.cleaned_data['recipient']
                    recipient = get_object_or_404(User, username=recipient_username)
                    recipient_wallet = get_object_or_404(UserWallet, user=recipient)
                    user_wallet.amount -= amount
                    user_wallet.save()
                    recipient_wallet.amount += amount
                    recipient_wallet.save()
                    user_wallet.save()
                    Transaction.objects.create(
    wallet=user_wallet,
    transaction_type=Transaction.TRANSFER,
    amount=amount,
    description=""
    
)
                    Transaction.objects.create(
    wallet=recipient_wallet,
    transaction_type=Transaction.FUND,
    amount=amount,
    description=""
)
                    messages.success(request, f'R {amount} was successfully transferred to {recipient_username}')
                    return redirect('wallet')
                else:
                    messages.error(request, f'You do not have R {amount} in your account')
                    return redirect('wallet')
            except Exception as e:
                messages.error(request, f'Wait a minute....Are you sure {recipient_username} exists?')
                return redirect('wallet')
        else:
            messages.error(request, "The input is invalid in form")
    return redirect('wallet')
