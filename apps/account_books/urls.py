from django.urls import path

from account_books.views import AccountRetrieveUpdateDestroyAPIView

app_name = 'account_books'

urlpatterns = [
    path('<int:book_id>/', AccountRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
]
