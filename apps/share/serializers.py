from rest_framework import serializers

from share.models import Guest


class GuestSerializer(serializers.ModelSerializer):

    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = Guest
        fields = (
            'code',
            'created_at',
            'updated_at',
            'object_pks',
            'access_scope',
            'expired_at',
            'is_expired',
            'created_by',
        )

    def get_is_expired(self, obj):
        return obj.is_expired
