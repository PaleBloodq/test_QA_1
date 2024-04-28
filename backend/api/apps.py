from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self) -> None:
        from api import signals
        signals.ready()
    
    # def ready(self) -> None:
        # from api import models
        # models.Tag.objects.get_or_create(name='Подписки EA Play', database_name='eaPlay')
        # models.Tag.objects.get_or_create(name='Подписки PS Plus', database_name='psPlus')
        # models.Tag.objects.get_or_create(name='Офферы', database_name='offers')
        # models.Tag.objects.get_or_create(name='Новинки', database_name='new')
        # models.Tag.objects.get_or_create(name='Лидеры продаж', database_name='leaders')
