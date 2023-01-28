from django.http import HttpResponseRedirect
from django.urls import reverse


def super_access(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('my_login'))
    return inner
