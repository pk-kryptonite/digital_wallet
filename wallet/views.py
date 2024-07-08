from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserWallet
from .forms import FundForm, TransferForm

@login_required
def wallet(request):
    if request.method == 'GET':
        user = request.user
       
        user_wallets = UserWallet.objects.filter(user=user)
        context = {
            'user': user.username,
            'user_wallets': user_wallets,
            "user_auth": user.is_authenticated
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
