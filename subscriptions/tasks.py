from celery import shared_task
from datetime import datetime
import requests
from decouple import config
from .models import ExchangeRateLog


@shared_task
def fetch_usd_to_bdt_exchange_rate():
    print("Fetching USD to BDT exchange rate...")
    base = 'USD'
    target = 'BDT'
    api_key = config('EXCHANGE_RATE_API_KEY')
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'conversion_rates' not in data or target not in data['conversion_rates']:
            return {'error': 'Invalid currency or API error'}
        
        rate = data['conversion_rates'][target]
        ExchangeRateLog.objects.create(
            base_currency=base,
            target_currency=target,
            rate=rate,
            fetched_at=datetime.now()
        )
        return {'base': base, 'target': target, 'exchange_rate': rate}
    except requests.RequestException as e:
        return {'error': str(e)}