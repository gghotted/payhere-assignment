from django.urls import path

from share.views import GuestRetrieveAPIView

app_name = 'share'

urlpatterns = [
    path('guests/<str:guest_code>/', GuestRetrieveAPIView.as_view(), name='detail_guest'),
]
