from django.contrib import admin
from django.db.models import QuerySet, ManyToManyField
from django.utils.html import format_html
from api import models, forms
from settings import FORCE_SCRIPT_NAME


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
    @admin.display(description='Изданий')
    def count_publications(self, obj: models.Product):
        count = models.Publication.objects.filter(product=obj).count()
        return format_html(f'<a href="{FORCE_SCRIPT_NAME}/admin/api/publication/?product__id__exact={obj.id}">{count}</a>')
    
    @admin.display(description='Аддонов')
    def count_add_ons(self, obj: models.Product):
        count = models.AddOn.objects.filter(product=obj).count()
        return format_html(f'<a href="{FORCE_SCRIPT_NAME}/admin/api/addon/?product__id__exact={obj.id}">{count}</a>')

    def parse_product_publications(self, request, queryset: QuerySet[models.Product]):
        from api import tasks
        tasks.parse_product_publications_task.delay([str(product.id) for product in queryset])
    parse_product_publications.short_description = 'Спарсить издания и аддоны'
    
    def delete_publications(self, request, queryset: QuerySet[models.Product]):
        models.Publication.objects.filter(
            product__in=queryset
        ).delete()
    delete_publications.short_description = 'Удалить издания'
    
    def delete_add_ons(self, request, queryset: QuerySet[models.Product]):
        models.AddOn.objects.filter(
            product__in=queryset
        ).delete()
    delete_add_ons.short_description = 'Удалить аддоны'

    list_filter = [PriceChangedListFilter]
    list_display = ['title', 'type', 'release_date', 'count_publications', 'count_add_ons', 'ps_store_url']
    readonly_fields = ['orders']
    actions = [parse_product_publications, delete_publications, delete_add_ons]
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


@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'product',
        'final_price',
        'ps_plus_final_price',
        'price_changed',
    ]
    list_filter = [
        'product',
        'price_changed',
    ]


@admin.register(models.AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'product',
        'final_price',
        'ps_plus_final_price',
        'price_changed',
    ]
    list_filter = [
        'product',
        'price_changed',
        'type',
    ]


@admin.register(models.AddOnType)
class AddOnTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'product',
        'final_price',
        'ps_plus_final_price',
        'price_changed',
    ]
    list_filter = [
        'product',
        'price_changed',
    ]
