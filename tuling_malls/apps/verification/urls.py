from django.urls import path
from verification import views
from utils.models import UUIDConverter
from django.urls import register_converter
register_converter(UUIDConverter,'uuid')
urlpatterns = [
    path('image_codes/<uuid:image_code_id>/', views.image_code_id.as_view()),
    path('sms_codes/<mobile>/',views.sms_codes.as_view())
]
