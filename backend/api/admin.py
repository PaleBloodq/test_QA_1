import logging
import os

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import QuerySet, ImageField, ForeignKey, ManyToManyField
from django.http import HttpRequest
from django.urls import reverse
from django.utils.safestring import mark_safe

from api import models, serializers
from settings import settings

PRODUCT_PARSER_URL = f'{os.environ.get("PRODUCT_PARSER_SCHEMA")}://{os.environ.get("PRODUCT_PARSER_HOST")}'
if os.environ.get("PRODUCT_PARSER_PORT"):
    PRODUCT_PARSER_URL += f':{os.environ.get("PRODUCT_PARSER_PORT")}'
PRODUCT_PARSER_URL += '/parse'

admin.site.register(models.Platform)

admin.site.register(models.Language)

admin.site.register(models.Tag)

admin.site.register(models.Profile)


class DragAndDropFileInput(forms.ClearableFileInput):
    template_name = 'admin/drag_and_drop_file_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['BASE_URL'] = settings.FORCE_SCRIPT_NAME
        return context


class ProductPublicationInline(admin.TabularInline):
    model = models.ProductPublication
    extra = 0
    readonly_fields = ('final_price', 'price_changed', )
    ordering = ('title',)
    exclude = ['hash']
    formfield_overrides = {
        ImageField: {'widget': DragAndDropFileInput},
    }

    def get_fields(self, request, obj=None):
        # Получить все поля модели
        fields = super().get_fields(request, obj)
        fields.remove('final_price')
        fields.insert(2, 'final_price')
        fields.remove('price_changed')
        fields.insert(3, 'price_changed')
        return fields

    def get_exclude(self, request, product: models.Product):
        if product:
            match product.type:
                case models.Product.TypeChoices.DONATION:
                    self.exclude += ['title', 'duration']
                case models.Product.TypeChoices.SUBSCRIPTION:
                    self.exclude += ['quantity']
                case models.Product.TypeChoices.GAME:
                    self.exclude += ['duration', 'quantity']
        return super().get_exclude(request, product)


@admin.register(models.Product, site=admin.site)
class ProductAdmin(admin.ModelAdmin):
    @admin.display(description='Количество изданий')
    def count_publications(self, obj: models.Product):
        return obj.publications.count()

    def parse_product_publications(self, request, queryset: QuerySet[models.Product]):
        from api import tasks
        data = serializers.ProductToParseSerializer(queryset, many=True).data
        tasks.parse_product_publications_task.delay(data)

    parse_product_publications.short_description = 'Спарсить издания'

    inlines = [ProductPublicationInline]
    list_display = ['title', 'type', 'release_date', 'count_publications']
    actions = [parse_product_publications]


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


@admin.register(models.Order, site=admin.site)
class OrderAdmin(admin.ModelAdmin):
    change_form_template = 'admin/order.html'
    inlines = [OrderProductInline]
    list_display = ['date', 'status', 'profile', 'amount']
    list_filter = ['date', 'status', 'profile', 'amount']
    readonly_fields = ['id']

    def render_change_form(self, request, context, add, change, form_url, obj):
        context.update({
            'FORCE_SCRIPT_NAME': settings.FORCE_SCRIPT_NAME,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


@admin.register(models.PromoCode, site=admin.site)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['promo_code', 'discount', 'expiration']
