from rest_framework.permissions import BasePermission


class IsOperatorOrSuperuser(BasePermission):
    """
    Allows access only to site operators (users in the 'Operator' group) or superusers.

    Usage:
        from apps.utils.auth.permissions import IsOperatorOrSuperuser

        class SomeView(APIView):
            permission_classes = [IsAuthenticated, IsOperatorOrSuperuser]
    """

    group_name = 'Operator'

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name=self.group_name).exists()
