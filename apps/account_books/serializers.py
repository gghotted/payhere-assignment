from core.serializers import CreateSerializer, UpdateSerializer
from rest_framework import serializers

from account_books.models import AccountBook


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
