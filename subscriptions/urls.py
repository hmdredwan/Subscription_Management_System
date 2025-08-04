from django.urls import path
from .views import SubscribeView, SubscriptionListView, CancelSubscriptionView, ExchangeRateView

urlpatterns = [
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscriptions'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel_subscription'),
    path('exchange-rate/', ExchangeRateView.as_view(), name='exchange_rate'),
]