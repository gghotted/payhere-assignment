from datetime import timedelta
from functools import cached_property, partial

from core.paginations import pagination_factory
from core.permissions import EqualUser
from core.views import CopyView
from django.shortcuts import get_object_or_404
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from share.permissions import IsGuest
from share.views import ShareLinkCreateAPIView

from account_books.models import AccountBook, Transaction
from account_books.serializers import (AccountBookCreateSerializer,
                                       AccountBookSerializer,
                                       AccountBookUpdateSerializer,
                                       TransactionCreateSerializer,
                                       TransactionSerializer,
                                       TransactionUpdateSerializer)


class AccountCreateListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AccountBookCreateSerializer
        return AccountBookSerializer

    def get_queryset(self):
        return self.request.user.account_books.all()


class AccountRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticated,
        partial(EqualUser, attr_name='user'),
    ]
    queryset = AccountBook.objects.all()
    lookup_url_kwarg = 'book_id'

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return AccountBookUpdateSerializer
        return AccountBookSerializer


class TransactionListCreateAPIView(ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
        partial(EqualUser, attr_name='user'),
    ]
    pagination_class = pagination_factory(page_size=10)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransactionCreateSerializer
        return TransactionSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['account_book'] = self.account_book
        return ctx

    def get_queryset(self):
        return self.account_book.transactions.all()

    @cached_property
    def account_book(self):
        obj = get_object_or_404(AccountBook, id=self.kwargs['book_id'])
        self.check_object_permissions(self.request, obj)
        return obj


class TransactionRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):
    user_permission = (
        IsAuthenticated &
        partial(EqualUser, attr_name='account_book.user')
    )
    guest_permission = partial(IsGuest, allowed_access_scope='view transaction {pk}')
    permission_classes = [user_permission | guest_permission]
    
    lookup_url_kwarg = 'transaction_id'
    queryset = Transaction.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return TransactionUpdateSerializer
        return TransactionSerializer


class TransactionCopyAPIView(CopyView):
    permission_classes = [
        IsAuthenticated,
        partial(EqualUser, attr_name='account_book.user'),
    ]
    lookup_url_kwarg = 'transaction_id'
    queryset = Transaction.objects.all()


class TransactionShareAPIView(ShareLinkCreateAPIView):
    permission_classes = [
        IsAuthenticated,
        partial(EqualUser, attr_name='account_book.user'),
    ]
    lookup_url_kwarg = 'transaction_id'
    queryset = Transaction.objects.all()

    share_access_scope = 'view transaction {pk}'
    share_link_host = 'https://front.com/'
    share_link_prefix = 's'
    share_life_time = timedelta(days=1)
