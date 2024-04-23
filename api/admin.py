from django.contrib import admin
from api import models


admin.site.register(models.Platform)


admin.site.register(models.Language)


admin.site.register(models.Tag)


admin.site.register(models.Profile)


class ProductPublicationInline(admin.TabularInline):
    model = models.ProductPublication
    extra = 0
    ordering = ('title', )
    
    def get_exclude(self, request, obj: models.Product):
        if obj:
            match obj.type:
                case models.Product.TypeChoices.DONATION:
                    return ('title', 'duration')
                case models.Product.TypeChoices.SUBSCRIPTION:
                    return ('quantity', )
                case models.Product.TypeChoices.GAME:
                    return ('duration', 'quantity')
                case _:
                    pass
        return super().get_exclude(request, obj)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    @admin.display(description='Количество изданий')
    def count_publications(self, obj: models.Product):
        return obj.publications.count()
    
    inlines = [ProductPublicationInline]
    list_display = ['title', 'type', 'release_date', 'count_publications']


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = ['date', 'status', 'profile', 'amount']
    list_filter = ['date', 'status', 'profile', 'amount']


@admin.register(models.PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['promo_code', 'discount', 'expiration']

class TestAdmin(admin.AdminSite):
    pass
