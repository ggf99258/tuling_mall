from django.urls import path
from user import views
from utils.models import MobileConverter,UsernameConverter
from django.urls import register_converter
register_converter(MobileConverter,'mobile')
register_converter(UsernameConverter,'usernames')
urlpatterns = [
    path('usernames/<usernames:username>/count/',views.usernames.as_view()),
    path('mobiles/<mobile:mobile>/count/',views.mobiles.as_view()),
    path('register/',views.register.as_view()),
    path('login/',views.logins.as_view()),
    path('logout/',views.logouts.as_view()),
    path('info/',views.info.as_view()),
    path('emails/',views.emails.as_view()),
    path('emails/verification/',views.emails_verification.as_view()),
    path('addresses/create/',views.addresses_create.as_view()),
    path('addresses/',views.addresses.as_view()),
    path('addresses/<id>/',views.addresses_id.as_view()),
    path('password/',views.password.as_view()),
    path('browse_histories/',views.browse_histories.as_view())
]
