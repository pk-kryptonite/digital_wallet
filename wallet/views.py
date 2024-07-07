from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserWallet, User
from .forms import FundForm, TransferForm

def wallet(request):
    user = get_object_or_404(User, id='6dcfdedb003348fa996d5ea57a208ca7')
    user_wallets = UserWallet.objects.filter(user=user)
    
    context = {
        'user': user.username,
        'user_wallets': user_wallets
    }
    
    return render(request, 'index.html', context)

def fund_wallet(request):
    if request.method == 'POST':
        form = FundForm(request.POST)
        if form.is_valid():
            try: 
                
                amount = form.cleaned_data['amount']
                wallet_id = form.cleaned_data['wallet_id']
                user_wallet = get_object_or_404(UserWallet, id=wallet_id)
                user_wallet.amount += amount
                user_wallet.save()
                messages.success(request, f'Wallet was successfully funded with R {amount}')
                return redirect('wallet')
            except Exception as e:
                messages.error(request, f'There was an error when funding wallet with R {amount}')
                return redirect('wallet')
    messages.error(request, f'There was an error when funding wallet with R {amount}')
    return redirect('wallet')

def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            try:  
                amount = form.cleaned_data['amount']
                wallet_id = form.cleaned_data['wallet_id']
                user_wallet = get_object_or_404(UserWallet, id=wallet_id)
                if amount <= user_wallet.amount:
                    recipient = form.cleaned_data['recipient']
                    user = get_object_or_404(User, username=recipient)
                    user_wallet.amount -= amount
                    user_wallet.save()
                    recipient_wallets = UserWallet.objects.filter(user=user)
                    #issue: if user has morethan one wallet, they would all receive transfer. NB: Need to be updated 
                    for wallet in recipient_wallets:
                        wallet.amount += amount
                        wallet.save()
                    messages.success(request, f'R {amount} was successfully transfered to {recipient}')
                    return redirect('wallet')
                else:
                    messages.error(request, f'You do not have R {amount} in your account')
                    return redirect('wallet')
            except Exception as e:
                messages.error(request, f'Wait a minute....Are you sure {recipient} exists?')
                return redirect('wallet')
   
    return redirect('wallet')