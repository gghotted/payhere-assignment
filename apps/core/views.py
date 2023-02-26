from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.serializers import CreateSerializer


class CopyModelMixin:

    def copy(self, request, *args, **kwargs):
        new_obj = self.get_object()
        new_obj.pk = None
        new_obj.save()

        return Response(
            CreateSerializer(new_obj).data,
            status=status.HTTP_201_CREATED,
        )


class CopyView(CopyModelMixin, GenericAPIView):

    def post(self, request, *args, **kwargs):
        return self.copy(request, *args, **kwargs)
