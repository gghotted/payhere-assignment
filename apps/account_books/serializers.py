from core.serializers import CreateSerializer, UpdateSerializer
from rest_framework import serializers

from account_books.models import AccountBook, Transaction


class AccountBookCreateSerializer(CreateSerializer):

    class Meta:
        model = AccountBook
        fields = (
            'name',
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AccountBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountBook
        fields = (
            'id',
            'created_at',
            'updated_at',
            'name',
        )


class AccountBookUpdateSerializer(UpdateSerializer):
    representation_serializer_class = AccountBookSerializer

    class Meta:
        model = AccountBook
        fields = (
            'name',
        )


class TransactionCreateSerializer(CreateSerializer):
    
    class Meta:
        model = Transaction
        fields = (
            'description',
            'occurred_at',
            'amount',
            'type',
        )

    def create(self, validated_data):
        validated_data['account_book'] = self.context['account_book']
        return super().create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            'id',
            'created_at',
            'updated_at',
            'description',
            'amount',
            'type',
            'occurred_at',
        )


class TransactionUpdateSerializer(UpdateSerializer):
    representation_serializer_class = TransactionSerializer

    class Meta:
        model = Transaction
        fields = (
            'description',
            'amount',
            'type',
            'occurred_at',
        )
