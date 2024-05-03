from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from admin_tools.menu import items, Menu

from settings import settings


class CustomMenu(Menu):
    """
    Custom Menu for aoki-bot admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem('Панель управления', reverse('admin:index')),
            items.MenuItem('Чаты', f'{settings.FORCE_SCRIPT_NAME}/admin/chat/'),
            items.AppList(
                'Приложения',
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                'Администрирование',
                models=('django.contrib.*',)
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
