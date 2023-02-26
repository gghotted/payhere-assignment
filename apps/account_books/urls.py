from django.urls import path

from account_books.views import (AccountRetrieveUpdateDestroyAPIView,
                                 TransactionCopyAPIView,
                                 TransactionListCreateAPIView,
                                 TransactionRetrieveUpdateDestroyAPIView)

app_name = 'account_books'

urlpatterns = [
    path('<int:book_id>/', AccountRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
    path('<int:book_id>/transactions/', TransactionListCreateAPIView.as_view(),
                                        name='list_transaction'),
    path('<int:book_id>/transactions/<int:transaction_id>/',
                                        TransactionRetrieveUpdateDestroyAPIView.as_view(),
                                        name='detail_transaction'),
    path('<int:book_id>/transactions/<int:transaction_id>/copy/',
                                        TransactionCopyAPIView.as_view(),
                                        name='copy_transaction'),
]
