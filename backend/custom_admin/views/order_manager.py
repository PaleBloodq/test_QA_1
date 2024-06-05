import logging
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView
from django.urls import reverse
from api import models


__all__ = [
    'OrderManager',
]


class OrderManager(TemplateView):
    template_name = 'order_manager/index.html'
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_staff:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                request.get_full_path(),
                reverse('admin:login'),
            )
        return super().get(request, *args, **kwargs)
