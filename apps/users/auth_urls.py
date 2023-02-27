from django.urls import path
from rest_framework_simplejwt.views import (TokenBlacklistView,
                                            TokenObtainPairView,
                                            TokenRefreshView)

app_name = 'auth'

urlpatterns = [
    path('tokens/', TokenObtainPairView.as_view(), name='create_token'),
    path('tokens/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('tokens/blacklist/', TokenBlacklistView.as_view(), name='blacklist_token'),
]
