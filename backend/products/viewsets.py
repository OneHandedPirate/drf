from rest_framework import viewsets, mixins

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    get -> list -> QuerySet
    get with pk -> retrieve -> Product Instance Detail View
    post -> create -> New Instance
    put -> Update
    patch -> Partial Update
    delete -> destroy instance
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' #default


class ProductGenericViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    """
    get -> list -> QuerySet
    get with pk -> retrieve -> Product Instance Detail View
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  # default


product_list_view = ProductGenericViewSet.as_view({'get': 'list'})
product_detail_view = ProductGenericViewSet.as_view({'get': 'retrieve'})