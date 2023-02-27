from datetime import timedelta

from django.utils.timezone import now
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from share.models import Guest
from share.utils import urljoin


class CreateShareLinkMixin:
    share_life_time = timedelta(hours=1)

    '''
    access_scope를 설정하고, 이 값으로 api 접근을 제어합니다.
    ex: "view user {pk}"
    '''
    share_access_scope = ''

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

    def share(self, request, *args, **kwargs):
        life_time = self.share_life_time
        access_scope = self.get_access_scope()
        link_host = self.share_link_host or self.request.get_host()
        link_prefix = self.share_link_prefix

        guest = Guest.objects.create(
            created_by=self.request.user,
            access_scope=access_scope,
            expired_at=(now() + life_time),
        )

        link = urljoin(link_host, link_prefix, guest.code)
        return Response(
            self.get_response_data(link),
            status=status.HTTP_200_OK,
        )

    def get_access_scope(self):
        if not self.share_access_scope:
            raise NotImplementedError(
                '"share_access_scope" must be set.'
            )

        share_access_scope = self.share_access_scope
        if '{pk}' in share_access_scope:
            obj = self.get_object()
            share_access_scope = share_access_scope.format(pk=obj.pk)
        return share_access_scope

    def get_response_data(self, link):
        return {'url': link}


class ShareLinkCreateAPIView(CreateShareLinkMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        return self.share(request, *args, **kwargs)
    