from rest_framework.permissions import BasePermission, SAFE_METHODS


ADMIN = "admin"
MANAGER = "manager"
WAREHOUSE_ROLES = {"warehouse", "warehouse_staff"}


def user_role(user):
    return getattr(user, "role", None)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and user_role(request.user) == ADMIN)


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and user_role(request.user) in {ADMIN, MANAGER}
        )


class IsAdminManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return user_role(request.user) in {ADMIN, MANAGER}


class IsAdminManagerOrWarehouseStaff(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return user_role(request.user) in {ADMIN, MANAGER, *WAREHOUSE_ROLES}
