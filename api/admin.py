from django.contrib import admin
from api import models

admin.site.register(models.Type)

admin.site.register(models.Platform)

admin.site.register(models.Language)

admin.site.register(models.Donation)

admin.site.register(models.Product)

admin.site.register(models.Tag)

######################################
# Удалить когда будет готова админка #
######################################

admin.site.register(models.DonationQuantity)

admin.site.register(models.ProductPublication)

admin.site.register(models.ProductDuration)

admin.site.register(models.ProductTag)

######################################
