import re
from datetime import timedelta
from functools import cached_property

from django.utils.timezone import now
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from share.models import Guest
from share.serializers import GuestSerializer
from share.utils import urljoin


class CreateShareLinkMixin:
    share_life_time = timedelta(hours=1)

    '''
    access_scope를 설정하고, 이 값으로 api 접근을 제어합니다.
    ex: ["view user {object.pk}"]
    '''
    share_access_scopes = None

    '''
    link의 호스트를 지정합니다.
    ex: https://front.com/
    '''
    share_link_host = ''

    '''
    link path prefix를 추가합니다.
    ex: 
        if share_link_prefix == 'share':
           link = 'https://front.com/share/{guest_code}/
    '''
    share_link_prefix = ''

    '''
    guest와 관련된 object의 pk의 list입니다.
    공유된 link에서 호출할 api의 endpoint를 빌드하는데 이용합니다.
    ex: [
        {
            'post': '{object.pk}',
            'user': '{object.user.pk}',
        }
    ]
    '''
    share_object_pks = None

    def share(self, request, *args, **kwargs):
        life_time = self.share_life_time
        access_scope = self.get_access_scope()
        object_pks = self.get_object_pks()
        link_host = self.share_link_host or self.request.get_host()
        link_prefix = self.share_link_prefix

        guest = Guest.objects.create(
            created_by=self.request.user,
            access_scope=access_scope,
            expired_at=(now() + life_time),
            object_pks=object_pks,
        )

        link = urljoin(link_host, link_prefix, guest.code)
        return Response(
            self.get_response_data(link),
            status=status.HTTP_200_OK,
        )

    def get_access_scope(self):
        if not self.share_access_scopes:
            raise NotImplementedError(
                '"share_access_scopes" must be set.'
            )

        return ','.join([
            self.convert_pk_format(access_scope)
            for access_scope in self.share_access_scopes
        ])

    def get_object_pks(self):
        if not self.share_object_pks:
            raise NotImplementedError(
                '"share_object_pks" must be set.'
            )

        return {
            key: self.convert_pk_format(val)
            for key, val in self.share_object_pks.items()
        }

    @cached_property
    def object(self):
        obj = self.get_object()
        return obj

    def convert_pk_format(self, format_str):
        pattern = re.compile(r'\{object.*\}')

        if pattern.findall(format_str):
            return format_str.format(object=self.object)
        
        return format_str

    def get_response_data(self, link):
        return {'url': link}


class ShareLinkCreateAPIView(CreateShareLinkMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        return self.share(request, *args, **kwargs)


class GuestRetrieveAPIView(RetrieveAPIView):
    serializer_class = GuestSerializer
    queryset = Guest.objects.all()
    lookup_url_kwarg = 'guest_code'
    lookup_field = 'code'
