from core.permissions import CallbleMixin
from django.utils.timezone import now
from rest_framework.permissions import BasePermission

from share.models import Guest


class IsGuest(CallbleMixin, BasePermission):
    allowed_methods = ['GET']

    def __init__(self, allowed_access_scope):
        self.allowed_access_scope = allowed_access_scope

    def has_guest_permission(self, request):
        guest_code = request.GET.get('guest')
        
        if not guest_code:
            return False
        
        qs = Guest.objects.filter(
            expired_at__gt=now(),
            code=guest_code,
            access_scope=self.allowed_access_scope
        )
        return qs.exists()
        

    def has_permission(self, request, view):
        lookup_url_kwarg = view.lookup_url_kwarg or view.lookup_field
        self.allowed_access_scope = self.allowed_access_scope.format(
            pk=view.kwargs[lookup_url_kwarg]
        )
        return (
            request.method in self.allowed_methods and
            self.has_guest_permission(request)
        )

    def has_object_permission(self, request, view, obj):
        self.allowed_access_scope = self.allowed_access_scope.format(pk=obj.pk)
        return (
            request.method in self.allowed_methods and
            self.has_guest_permission(request)
        )
