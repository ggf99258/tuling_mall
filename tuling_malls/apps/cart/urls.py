from django.urls import path
from . import views
urlpatterns = [
    path('carts/',views.carts.as_view()),
    path('carts/selection/',views.carts_selection.as_view()),
    path('carts/simple/',views.carts_simple.as_view()),
    path('orders/settlement/',views.orders_settlement.as_view()),
    path('orders/commit/',views.orders_commit.as_view())
]