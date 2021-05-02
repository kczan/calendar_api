from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class RegistrationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        else:
            return bool(request.user and request.user.is_authenticated)


class RegistrationAuthentication(TokenAuthentication):
    def authenticate(self, request):
        if request.method == 'POST':
            return None
        return super().authenticate(request)