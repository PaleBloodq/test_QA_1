from django.contrib import admin
from api import models

admin.site.register(models.Platform)

admin.site.register(models.Language)

admin.site.register(models.Tag)

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

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPublicationInline]

admin.site.register(models.Product, ProductAdmin)

class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]

admin.site.register(models.Order, OrderAdmin)

admin.site.register(models.Profile)
