from rest_framework import serializers


class CreateSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'created_at': instance.created_at,
        }
