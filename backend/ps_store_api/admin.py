from django.contrib import admin
from . import models


@admin.register(models.Concept)
class ConceptAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AddOn)
class AddOnAdmin(admin.ModelAdmin):
    pass
