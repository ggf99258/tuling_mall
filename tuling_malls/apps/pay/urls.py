from django.urls import path
from . import views
urlpatterns = [
    path('payment/<order_id>/', views.payment_order_id.as_view()),
    path('payment/status/',views.order_string.as_view())
]