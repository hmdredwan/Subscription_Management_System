from django.urls import path, include
from django.contrib import admin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from subscriptions.views import subscription_list

class RootView(APIView):
       def get(self, request):
           return Response({
               'message': 'Welcome to the Subscription Management API',
               'endpoints': {
                   'token': '/api/token/',
                   'token_refresh': '/api/token/refresh/',
                   'subscribe': '/api/subscribe/',
                   'subscriptions': '/api/subscriptions/',
                   'cancel_subscription': '/api/cancel/',
                   'exchange_rate': '/api/exchange-rate/?base=USD&target=BDT',
                   'frontend_subscriptions': '/subscriptions/'
               }
           })

def redirect_to_api(request):
    return HttpResponseRedirect('/api/exchange-rate/?base=USD&target=BDT')

urlpatterns = [
    path('', RootView.as_view(), name='root'),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('subscriptions.urls')),
    path('subscriptions/', subscription_list, name='subscription_list'),
]