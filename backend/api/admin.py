from django.contrib import admin
from django.db.models import QuerySet, ImageField, ManyToManyField
from api import models, forms

class ProductPublicationInline(admin.StackedInline):
    model = models.ProductPublication
    extra = 0
    readonly_fields = ('price_changed',)
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
        tasks.parse_product_publications_task.delay([str(product.id) for product in queryset])
    parse_product_publications.short_description = 'Спарсить издания'
    
    def delete_publications(self, request, queryset: QuerySet[models.Product]):
        models.ProductPublication.objects.filter(
            product__in=queryset
        ).delete()
    delete_publications.short_description = 'Удалить издания'

    inlines = [ProductPublicationInline]
    list_filter = [PriceChangedListFilter]
    list_display = ['title', 'type', 'release_date', 'count_publications', 'price_changed']
    readonly_fields = ['orders']
    actions = [parse_product_publications, delete_publications]
    formfield_overrides = {
        ManyToManyField: {'widget': forms.ManyToManyForm},
    }


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = ['date', 'status', 'profile', 'amount']
    list_filter = ['date', 'status', 'profile', 'amount']
    readonly_fields = ['id', 'payment_id', 'payment_url']
    search_fields = ['id', 'profile__telegram_id', 'amount']


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


class MailingMediaInline(admin.TabularInline):
    model = models.MailingMedia
    extra = 0


@admin.register(models.Mailing)
class MailingAdmin(admin.ModelAdmin):
    inlines = [MailingMediaInline]
    readonly_fields = ['sent_count', 'received_count']
    list_display = ['start_on', 'status', 'text']
    list_filter = ['start_on', 'status']
