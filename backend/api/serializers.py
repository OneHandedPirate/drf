from rest_framework import serializers


class UserProductInLineSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product_detail',
        lookup_field='pk',
        read_only=True
    )


class UserPublicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    # other_products = serializers.SerializerMethodField(read_only=True)
    #
    # def get_other_products(self, obj):
    #     request = self.context.get('request')
    #     user = obj
    #     my_products_qs = user.product_set.all()[:5]
    #     return UserProductInLineSerializer(my_products_qs,
    #                                        many=True,
    #                                        # context={'request': request}).data
    #                                        context=self.context).data
