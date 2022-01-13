from django.urls import path
from . import views
urlpatterns = [
    path('areas/',views.areas.as_view()),
    path('areas/<int:id>/',views.areas_id.as_view()),
]
