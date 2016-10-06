#coding:utf-8

from django.http import HttpResponseRedirect




def group_required(function=None, group=None, redirect_url=None):

    def _dec(func):
        def _view(request, *args, **kwargs):
            for g in request.user.groups.values_list():
                if g[1] == group:
                    return func(request, *args, **kwargs)

            return HttpResponseRedirect(redirect_url)


        _view.__name__ = func.__name__
        _view.__dict__ = func.__dict__
        _view.__doc__ = func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)




def anonymous_required(function=None, home_url=None, redirect_field_name=None):
    """Check that the user is NOT logged in.

    This decorator ensures that the view functions it is called on can be
    accessed only by anonymous users. When an authenticated user accesses
    such a protected view, they are redirected to the address specified in
    the field named in `next_field` or, lacking such a value, the URL in
    `home_url`, or the `USER_HOME_URL` setting.
    """
    if home_url is None:
        home_url = "/"

    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if request.user.is_authenticated():
                url = None
                if redirect_field_name and redirect_field_name in request.REQUEST:
                    url = request.REQUEST[redirect_field_name]
                if not url:
                    url = home_url
                if not url:
                    url = "/"
                return HttpResponseRedirect(url)
            else:
                return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)