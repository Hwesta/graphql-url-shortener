from django.shortcuts import get_object_or_404, redirect

from . import models


def redirect_short_url(request, short_url):
    """Redirect the short URL to the original URL"""
    mapping = get_object_or_404(models.URLMapping, short_url=short_url)
    return redirect(to=mapping.original_url)
