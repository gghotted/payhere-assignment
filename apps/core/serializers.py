from rest_framework import serializers


class CreateSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'created_at': instance.created_at,
        }


class UpdateSerializer(serializers.ModelSerializer):
    representation_serializer_class = None

    def to_representation(self, instance):
        return self.representation_serializer_class(
            instance=instance
        ).data
