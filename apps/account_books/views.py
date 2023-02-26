from functools import partial

from core.permissions import EqualUser
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from account_books.models import AccountBook
from account_books.serializers import (AccountBookCreateSerializer,
                                       AccountBookSerializer,
                                       AccountBookUpdateSerializer)


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
