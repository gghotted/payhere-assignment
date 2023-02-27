from account_books.views import AccountCreateListCreateAPIView
from django.urls import path

from users.views import UserCreateAPIView

app_name = 'users'

urlpatterns = [
    path('', UserCreateAPIView.as_view(), name='create'),

    # account_books
    path('self/account-books/', AccountCreateListCreateAPIView.as_view(), name='list_account_book'),
]
