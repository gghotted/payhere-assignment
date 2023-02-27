from django.db.models import Manager
from django.db.models.aggregates import Sum
from django.db.models.expressions import Q


class AccountBookManager(Manager):
    def get_queryset(self):
        total_amount = (
            Sum('transactions__amount', filter=Q(transactions__type='+')) -
            Sum('transactions__amount', filter=Q(transactions__type='-'))
        )
        return super().get_queryset().annotate(
            total_amount=total_amount
        )
