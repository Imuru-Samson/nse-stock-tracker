from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from .models import Stock

def welcome_view(request):
    return render(request, 'stocks/welcome.html')  # Make sure this template exists

def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stocks/stock_list.html', {'stocks': stocks})

def stock_detail(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol.upper())
    return render(request, 'stocks/stock_detail.html', {'stock': stock})

def live_price(request, symbol):
    try:
        stock = Stock.objects.get(symbol=symbol.upper())
        return JsonResponse({
            'symbol': stock.symbol,
            'price': str(stock.price),
            'time': datetime.now().strftime('%H:%M:%S')
        })
    except Stock.DoesNotExist:
        return JsonResponse({
            'symbol': symbol.upper(),
            'price': '0.00',
            'time': datetime.now().strftime('%H:%M:%S')
        }, status=404)
