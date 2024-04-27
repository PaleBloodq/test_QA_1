from rest_framework import serializers
from api import models, utils


class EnumSerializer(serializers.RelatedField):
    def to_representation(self, value: models.EnumBaseModel):
        return value.name
    

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Platform
        fields = (
            'id',
            'name',
        )


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Platform
        fields = (
            'id',
            'name',
        )

class ProductPublicationSerializer(serializers.ModelSerializer):
    platforms = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.ProductPublication
        fields = (
            'id',
            'title',
            'final_price',
            'original_price',
            'duration',
            'quantity',
            'includes',
            'platforms',
            'preview',
            'photo',
            'cashback',
            'ps_plus_discount',
            'discount',
            'discount_deadline',
        )


class ProductSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    publications = ProductPublicationSerializer(many=True)
    languages = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Product
        fields = (
            'id',
            'title',
            'type',
            'languages',
            'release_date',
            'publications',
        )


class SingleProductSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    languages = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Product
        fields = (
            'id',
            'title',
            'type',
            'languages',
            'release_date',
        )


class SingleProductPublicationSerializer(serializers.ModelSerializer):
    product = SingleProductSerializer()
    platforms = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.ProductPublication
        fields = (
            'id',
            'title',
            'price',
            'duration',
            'quantity',
            'includes',
            'platforms',
            'preview',
            'photo',
            'cashback',
            'ps_plus_discount',
            'discount',
            'discount_deadline',
            'product',
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = (
            'playstation_email',
            'playstation_password',
            'bill_email',
            'cashback',
        )


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderProduct
        fields = (
            'item',
            'description',
            'price',
        )


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)
    
    class Meta:
        model = models.Order
        fields = (
            'date',
            'amount',
            'status',
            'order_products',
        )


class UpdateProductPublicationSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    platforms = serializers.ListField(required=True)
    final_price = serializers.IntegerField(required=True)
    original_price = serializers.IntegerField(required=True)
    offer_ends = serializers.DateTimeField(allow_null=True)
    discount = serializers.IntegerField(allow_null=True)
    
    def save(self, product: models.Product):
        title = self.validated_data.get('title')
        platforms = self.validated_data.get('platforms')
        final_price = self.validated_data.get('final_price')
        original_price = self.validated_data.get('original_price')
        offer_ends = self.validated_data.get('offer_ends')
        discount = self.validated_data.get('discount')
        hash = utils.hash_product_publication(
            product.id,
            title,
            [platform for platform in platforms]
        )
        publication = models.ProductPublication.objects.filter(hash=hash)
        if publication:
            publication = publication.first()
            publication.final_price = final_price
            publication.original_price = original_price
            publication.discount_deadline = offer_ends
            publication.discount = discount
        else:
            publication = models.ProductPublication(
                product=product,
                title=title,
                final_price=final_price,
                original_price=original_price,
                discount_deadline=offer_ends,
                discount=discount
            )
            publication.save()
            for platform in platforms:
                publication.platforms.add(models.Platform.objects.get_or_create(name=platform)[0])
            publication.hash = hash
        publication.save()
        return publication
