from django.contrib import admin
from django.urls import path, include
from stocks.views import welcome_view  # Import the landing view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_view, name='welcome'),  # 👈 Landing page
    path('stocks/', include('stocks.urls')),
]
