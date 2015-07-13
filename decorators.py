from functools import wraps

from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.utils.decorators import available_attrs
from django.utils.six.moves.urllib.parse import urlparse


def token_or_login_required(view_func):
    """
    Merger of the login_required and roken_required decorators
    It will attempt to auth tokens if it finds one, otherwise, it will fall back to a normal login.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = None
        token = None
        basic_auth = request.META.get('HTTP_AUTHORIZATION')

        user = request.POST.get('user', request.GET.get('user'))
        token = request.POST.get('token', request.GET.get('token'))

        if not (user and token) and basic_auth:
            auth_method, auth_string = basic_auth.split(' ', 1)

            if auth_method.lower() == 'basic':
                auth_string = auth_string.strip().decode('base64')
                user, token = auth_string.split(':', 1)

        path = request.build_absolute_uri()
        resolved_login_url = resolve_url(settings.LOGIN_URL)
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if ((not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)):
            path = request.get_full_path()
        from django.contrib.auth.views import redirect_to_login
        login_view = redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)

        if not (user and token):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
        else:
            user = authenticate(pk=user, token=token)
            if user:
                login(request, user)
                return view_func(request, *args, **kwargs)
        return login_view
    return _wrapped_view
