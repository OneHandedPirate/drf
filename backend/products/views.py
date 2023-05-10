from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer
from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin


class ProductListCreateAPIView(StaffEditorPermissionMixin,
                               UserQuerySetMixin,
                               generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('price')
    serializer_class = ProductSerializer


    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     print('Hello there!')
    #     request = self.request
    #     user = request.user
    #     print(user)
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=request.user)


class ProductDetailAPIView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        serializer.save()


class ProductDeleteAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductMixinView(
    StaffEditorPermissionMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = 'This is a single view doing cool stuff'
        serializer.save(content=content)


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == 'GET':
        if pk:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        qs = Product.objects.all()
        data = ProductSerializer(qs, many=True).data
        return Response(data)
    elif method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            content = serializer.validated_data.get('content', None)
            if not content:
                content = serializer.validated_data.get('title')
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({'invalid': 'Data is not valid'})


