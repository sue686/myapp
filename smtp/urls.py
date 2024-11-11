# urls.py
from django.urls import path
from .views import SendEmailView

urlpatterns = [
    path('', SendEmailView.as_view(), name='send-email'),
]
