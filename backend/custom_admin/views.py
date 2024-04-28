from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from api import models
from custom_admin import forms

class Chat(TemplateView):
    template_name = 'admin/chat.html'
    
    def get(self, request: HttpRequest, order_id=None) -> HttpResponse:
        if order_id:
            try:
                order = models.Order.objects.get(id=order_id)
                form = forms.SendChatMessageForm()
                return super().get(request, order=order, form=form)
            except:
                pass
        return super().get(request)
    
    def post(self, request: HttpRequest, order_id) -> HttpResponse:
        form = forms.SendChatMessageForm(request.POST)
        if form.is_valid():
            form.instance.order = models.Order.objects.get(id=order_id)
            form.instance.manager = request.user
            form.save()
        form = forms.SendChatMessageForm()
        return self.get(request, order_id)
