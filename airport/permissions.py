from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    The Request is authenticated as admin user,
    or is a read-only non-admin users requests.
    """

    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission class that allows write access only to admin users,
    while allowing read access to all users, including anonim user.
    """

    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
            )
            or (request.user and request.user.is_staff)
        )
