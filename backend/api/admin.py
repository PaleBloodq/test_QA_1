from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import mark_safe
from api import models


admin.site.register(models.Platform)


admin.site.register(models.Language)


admin.site.register(models.Tag)


admin.site.register(models.Profile)


class ProductPublicationInline(admin.TabularInline):
    model = models.ProductPublication
    extra = 0
    ordering = ('title', )
    exclude = ['hash']
    
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
    
    inlines = [ProductPublicationInline]
    list_display = ['title', 'type', 'release_date', 'count_publications']


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 0


class ChatMessageInline(admin.TabularInline):
    model = models.ChatMessage
    extra = 0
    ordering = ('-created_at', )
    fields = ('created_at', 'sender', 'text', )
    readonly_fields = ('created_at', 'sender', 'text', )
    show_change_link = True
    
    def sender(self, obj: models.ChatMessage):
        if obj.manager:
            return mark_safe(f'<a href="/admin/auth/user/{obj.manager.pk}/">Менеджер {obj.manager}</a>')
        return mark_safe(f'<a href="/admin/api/profile/{obj.order.profile.id}/">Клиент {obj.order.profile.telegram_id}</a>')
    
    def has_change_permission(self, request: HttpRequest, obj) -> bool:
        return False


@admin.register(models.Order, site=admin.site)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline, ChatMessageInline]
    list_display = ['date', 'status', 'profile', 'amount', 'chat']
    list_filter = ['date', 'status', 'profile', 'amount']
    
    @admin.display(description='Чат')
    def chat(self, obj: models.Order):
        return mark_safe(f'<a href="/admin/chat/{obj.id}/">Открыть чат</a>')


@admin.register(models.PromoCode, site=admin.site)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['promo_code', 'discount', 'expiration']
