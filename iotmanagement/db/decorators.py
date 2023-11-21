from functools import wraps
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Assuming your user profile is accessible via request.user.userprofile
        user_profile = getattr(request.user, 'userprofile', None)

        if user_profile and user_profile.is_admin():
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return _wrapped_view
