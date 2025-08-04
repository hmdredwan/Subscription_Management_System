from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Plan, Subscription, ExchangeRateLog
import requests
from decouple import config
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.models import User


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from .serializers import SubscriptionSerializer
        plan_id = request.data.get('plan_id')
        try:
            plan = Plan.objects.get(id=plan_id)
            subscription, created = Subscription.objects.get_or_create(
                user=request.user,
                plan=plan,
                defaults={
                    'status': 'active',
                    'start_date': datetime.now(),
                    'end_date': datetime.now() + timedelta(days=plan.duration_days)
                }
            )
            if not created:
                return Response({'error': 'Subscription already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Plan.DoesNotExist:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)

class SubscriptionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from .serializers import SubscriptionSerializer
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription_id = request.data.get('subscription_id')
        try:
            subscription = Subscription.objects.get(id=subscription_id, user=request.user)
            subscription.status = 'cancelled'
            subscription.save()
            return Response({'message': 'Subscription cancelled'}, status=status.HTTP_200_OK)
        except Subscription.DoesNotExist:
            return Response({'error': 'Subscription not found'}, status=status.HTTP_404_NOT_FOUND)

class ExchangeRateView(APIView):
    def get(self, request):
        base = request.query_params.get('base', 'USD')
        target = request.query_params.get('target', 'BDT')
        api_key = config('EXCHANGE_RATE_API_KEY')
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'conversion_rates' not in data or target not in data['conversion_rates']:
                return Response({'error': 'Invalid currency or API error'}, status=status.HTTP_400_BAD_REQUEST)
            
            rate = data['conversion_rates'][target]
            ExchangeRateLog.objects.create(
                base_currency=base,
                target_currency=target,
                rate=rate,
                fetched_at=datetime.now()
            )
            return Response({
                'base': base,
                'target': target,
                'exchange_rate': rate,
                'timestamp': datetime.now()
            }, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def subscription_list(request):
       subscriptions = Subscription.objects.select_related('user', 'plan').all()
       return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subscriptions})