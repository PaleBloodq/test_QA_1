from django.contrib import admin
from api import models

admin.site.register(models.Platform)

admin.site.register(models.Language)

admin.site.register(models.Tag)

class ProductPublicationInline(admin.StackedInline):
    model = models.ProductPublication
    extra = 0
    
    def get_exclude(self, request, obj: models.Product):
        match obj.type:
            case models.Product.TypeChoices.DONATION:
                return ('title', 'duration')
            case models.Product.TypeChoices.SUBSCRIPTION:
                return ('quantity', )
            case models.Product.TypeChoices.GAME:
                return ('duration', 'quantity')
            case _:
                return super().get_exclude(request, obj)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPublicationInline]

admin.site.register(models.Product, ProductAdmin)
