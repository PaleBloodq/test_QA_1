from django.contrib import admin
from api import models

admin.site.register(models.Type)

admin.site.register(models.Platform)

admin.site.register(models.Language)

admin.site.register(models.Donation)

admin.site.register(models.Product)
