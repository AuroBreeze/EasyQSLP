from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed, PermissionDenied


def custom_exception_handler(exc, context):
    """
    Unify auth-related error responses:
    - NotAuthenticated -> {"success": False, "message": "Invalid credentials", "errors": {"ValidationError": "未提供认证凭据"}}
    - AuthenticationFailed -> {"success": False, "message": "Invalid credentials", "errors": {"ValidationError": "认证失败"}}
    - PermissionDenied -> {"success": False, "message": "Permission denied", "errors": {"ValidationError": "没有权限"}}
    Falls back to DRF default for others.
    """
    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        return Response({
            "success": False,
            "message": "Invalid credentials",
            "errors": {"ValidationError": "未提供认证凭据"}
        }, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, AuthenticationFailed):
        return Response({
            "success": False,
            "message": "Invalid credentials",
            "errors": {"ValidationError": "认证失败"}
        }, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, PermissionDenied):
        return Response({
            "success": False,
            "message": "Permission denied",
            "errors": {"ValidationError": "没有权限"}
        }, status=status.HTTP_403_FORBIDDEN)

    # If DRF produced a response, optionally normalize 'detail' for consistency
    if response is not None and isinstance(response.data, dict) and 'detail' in response.data:
        # Preserve status code but wrap the detail
        msg = response.data.get('detail') or '错误'
        # Choose a generic message label depending on status
        generic_msg = "Invalid data"
        if response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN):
            generic_msg = "Invalid credentials" if response.status_code == 401 else "Permission denied"
        response.data = {
            "success": False,
            "message": generic_msg,
            "errors": {"ValidationError": str(msg)}
        }
        return response

    return response
