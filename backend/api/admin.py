import logging
import os

from django.contrib import admin
from django.db.models import QuerySet, ImageField, ManyToManyField
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from api import models, serializers, forms
from settings import settings


PRODUCT_PARSER_URL = f'{os.environ.get("PRODUCT_PARSER_SCHEMA")}://{os.environ.get("PRODUCT_PARSER_HOST")}'
if os.environ.get("PRODUCT_PARSER_PORT"):
    PRODUCT_PARSER_URL += f':{os.environ.get("PRODUCT_PARSER_PORT")}'
PRODUCT_PARSER_URL += '/parse'


class ProductPublicationInline(admin.TabularInline):
    model = models.ProductPublication
    extra = 0
    readonly_fields = ('final_price', 'price_changed',)
    ordering = ('title',)
    exclude = ['hash']
    formfield_overrides = {
        ImageField: {'widget': forms.DragAndDropFileInput},
        ManyToManyField: {'widget': forms.ManyToManyForm},
    }

    def get_fields(self, request, obj: models.Product = None):
        # Получить все поля модели
        fields = super().get_fields(request, obj)
        if obj:
            match obj.type:
                case models.Product.TypeChoices.DONATION:
                    fields.remove('title')
                    fields.remove('duration')
                case models.Product.TypeChoices.SUBSCRIPTION:
                    fields.remove('quantity')
                case models.Product.TypeChoices.GAME:
                    fields.remove('duration')
                    fields.remove('quantity')
        fields.remove('final_price')
        fields.insert(2, 'final_price')
        fields.remove('price_changed')
        fields.insert(3, 'price_changed')
        return fields


class PriceChangedListFilter(admin.SimpleListFilter):
    title = 'Цена изменилась?'
    parameter_name = 'price_changed'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(publications__price_changed=True).distinct()
        if self.value() == 'no':
            return queryset.exclude(publications__price_changed=True).distinct()


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    @admin.display(description='Количество изданий')
    def count_publications(self, obj: models.Product):
        return obj.publications.count()

    @admin.display(description='Цена изменилась?', boolean=True)
    def price_changed(self, obj: models.Product):
        return obj.publications.filter(price_changed=True).exists()


    def parse_product_publications(self, request, queryset: QuerySet[models.Product]):
        from api import tasks
        data = serializers.ProductToParseSerializer(queryset, many=True).data
        tasks.parse_product_publications_task.delay(data)

    parse_product_publications.short_description = 'Спарсить издания'

    inlines = [ProductPublicationInline]
    list_filter = [PriceChangedListFilter]
    list_display = ['title', 'type', 'release_date', 'count_publications', 'price_changed']
    actions = [parse_product_publications]
    formfield_overrides = {
        ManyToManyField: {'widget': forms.ManyToManyForm},
    }


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 0


class ChatMessageInline(admin.TabularInline):
    model = models.ChatMessage
    extra = 0
    ordering = ('-created_at',)
    fields = ('created_at', 'sender', 'text',)
    readonly_fields = ('created_at', 'sender', 'text',)
    show_change_link = True

    def sender(self, obj: models.ChatMessage):
        if obj.manager:
            return mark_safe(
                f'<a href="{settings.FORCE_SCRIPT_NAME}/admin/auth/user/{obj.manager.pk}/">Менеджер {obj.manager}</a>')
        return mark_safe(
            f'<a href="{settings.FORCE_SCRIPT_NAME}/backend/admin/api/profile/{obj.order.profile.id}/">Клиент {obj.order.profile.telegram_id}</a>')

    def has_change_permission(self, request: HttpRequest, obj) -> bool:
        return False


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    change_form_template = 'admin/order.html'
    inlines = [OrderProductInline]
    list_display = ['date', 'status', 'profile', 'amount']
    list_filter = ['date', 'status', 'profile', 'amount']
    readonly_fields = ['id']
    search_fields = ['id', 'profile__telegram_id', 'amount']

    def render_change_form(self, request, context, add, change, form_url, obj):
        context.update({
            'FORCE_SCRIPT_NAME': settings.FORCE_SCRIPT_NAME,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


@admin.register(models.PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['promo_code', 'discount', 'expiration']


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ManyToManyField: {'widget': forms.ManyToManyForm},
    }


@admin.register(models.Platform)
class PlatformAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
