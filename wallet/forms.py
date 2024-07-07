from django import forms

class FundForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, label="Amount (R)")
    wallet_id = forms.CharField(label='Wallet ID', max_length=100)

class TransferForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, label="Amount (R)")
    recipient = forms.CharField(label='recipient username', max_length=150)
    wallet_id = forms.CharField(label='Wallet ID', max_length=100)