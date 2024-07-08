from django.urls import path
from .views import user_login, logout_view, register

urlpatterns = [
    path('login/', user_login, name='login'),
     path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
]
