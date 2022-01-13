from django.urls import path
from . import views
urlpatterns = [
    path('index/',views.index.as_view()),
    path('search/',views.search()),
    path('list/<int:id>/skus/',views.list_skus.as_view()),
    path('hot/<id>/',views.hot_sku.as_view()),
    path('goods/<id>',views.goods_id.as_view()),
    path('detail/visit/<id>/',views.detail_visit.as_view()),

]
