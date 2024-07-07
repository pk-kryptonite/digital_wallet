from django.urls import path
from .views import wallet, fund_wallet, transfer_funds

urlpatterns = [
    path('wallet/', wallet, name='wallet'),
    path('fund-wallet/', fund_wallet, name='fund_wallet'),
     path('transfer-funds/', transfer_funds, name='transfer_funds'),
  
]

