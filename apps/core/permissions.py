from operator import attrgetter

from rest_framework.permissions import BasePermission


class CallbleMixin:
    
    def __call__(self):
        return self


class EqualUser(CallbleMixin, BasePermission):

    def __init__(self, attr_name):
        self.attr_name = attr_name

    def has_object_permission(self, request, view, obj):
        return request.user == attrgetter(self.attr_name)(obj)
