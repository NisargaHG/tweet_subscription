from django.urls import path,include
from . import views

urlpatterns = [
    
    path('plans/', views.pay, name='pay'),
    path('accounts/', include('django.contrib.auth.urls')),
    
]
