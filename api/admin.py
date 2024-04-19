from django.contrib import admin
from api import models

admin.site.register(models.Type)

admin.site.register(models.Platform)

admin.site.register(models.Language)

class DonationQuantityInline(admin.StackedInline):
    model = models.DonationQuantity
    extra = 0

class DonationAdmin(admin.ModelAdmin):
    inlines = [DonationQuantityInline]

admin.site.register(models.Donation, DonationAdmin)

class ProductTagInline(admin.StackedInline):
    model = models.ProductTag
    extra = 0

class TagAdmin(admin.ModelAdmin):
    inlines = [ProductTagInline]

admin.site.register(models.Tag, TagAdmin)

class ProductPublicationInline(admin.StackedInline):
    model = models.ProductPublication
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPublicationInline]

admin.site.register(models.Product, ProductAdmin)
