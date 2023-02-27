from rest_framework.generics import CreateAPIView

from users.serializers import UserCreateSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
