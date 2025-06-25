from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import Stock

# Homepage / list of stocks
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stocks/stock_list.html', {'stocks': stocks})

# Detail page for an individual stock
def stock_detail(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol.upper())
    return render(request, 'stocks/stock_detail.html', {'stock': stock})

# Live price API endpoint
def live_price(request):
    symbol = request.GET.get('symbol', '').upper()
    try:
        stock = Stock.objects.get(symbol=symbol)
        return JsonResponse({
            'symbol': stock.symbol,
            'price': str(stock.price),
            'time': datetime.now().strftime('%H:%M:%S')
        })
    except Stock.DoesNotExist:
        return JsonResponse({
            'symbol': symbol,
            'price': '0.00',
            'time': datetime.now().strftime('%H:%M:%S')
        }, status=404)
