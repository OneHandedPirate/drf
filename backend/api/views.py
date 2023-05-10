import json

# from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products.serializers import ProductSerializer

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    # instance = Product.objects.all().order_by('?').first()
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # instance = serializer.save()
        # print(instance)
        print(serializer.data)
        return Response(serializer.data)
    return Response({'detail': 'Data is not valid'})
