from django.forms import ModelForm
from api import models

class SendChatMessageForm(ModelForm):
    class Meta:
        model = models.ChatMessage
        fields = ['text']
