from core.serializers import CreateSerializer
from rest_framework import serializers

from users.models import User


class UserCreateSerializer(CreateSerializer):
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'password2',
        )

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password2': 'password와 일치하지 않습니다.'}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
