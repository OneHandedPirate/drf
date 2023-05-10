from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError

from .models import Product
from .validators import validate_title_length, validate_title_no_hello, unique_product_title
from api.serializers import UserPublicSerializer


class ProductInLineSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product_detail',
        lookup_field='pk',
        read_only=True
    )


class ProductSerializer(serializers.ModelSerializer):

    update_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product_detail',
        lookup_field='pk',
    )
    title = serializers.CharField(validators=[validate_title_length,
                                              validate_title_no_hello,
                                              unique_product_title])

    username = serializers.CharField(source='user.username', read_only=True)
    owner = UserPublicSerializer(source='user', read_only=True)

    # name = serializers.CharField(source='title', read_only=True)
    # email = serializers.EmailField(write_only=True)
    # my_discount = serializers.SerializerMethodField(read_only=True)
    # url = serializers.SerializerMethodField(read_only=True)
    # related_products = ProductInLineSerializer(source='user.product_set.all',
    # many=True,
    # read_only=True)

    class Meta:
        model = Product

        fields = (
            'owner',
            'username',
            'pk',
            'url',
            'update_url',
            'title',
            'content',
            'price',
            'sale_price',
            # 'name',
            # 'email',
            # 'my_discount',
            #'related_products',
        )

    def get_update_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product_update", kwargs={"pk": obj.pk}, request=request)

    # # Additional fields validation within serializer class
    # def validate_title(self, value):
    #     request = self.context.get('request')
    #     user = request.user
    #     if Product.objects.filter(title__iexact=value).exists():
    #         raise ValidationError('The product title should be unique')
    #     if len(value) < 5:
    #         raise ValidationError('Title is too short')
    #     return value

    # def get_url(self, obj):
    #     """Получение абсолютной ссылки"""
    #
    #     request = self.context.get('request')
    #     if request is None:
    #         return None
    #     return reverse("product_detail", kwargs={"pk": obj.pk}, request=request)
    # def create(self, validated_data):
    #     email = validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     print(email, obj)
    #     return obj
    #
    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     print(email)
    #     return super().update(instance, validated_data)

    # @staticmethod
    # def get_my_discount(obj):
    #     try:
    #         return obj.get_discount()
    #     except:
    #         return None


