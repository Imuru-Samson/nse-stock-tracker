from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_list, name='stock_list'),  # <== This handles /stocks/
    path('welcome/', views.welcome_view, name='welcome_view'),
    path('<str:symbol>/', views.stock_detail, name='stock_detail'),
    path('<str:symbol>/live-price/', views.live_price, name='live_price'),
    path('live-price/', views.live_price, name='live_price'),  # ✅ This is the missing part
]

