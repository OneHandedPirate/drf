from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from products.models import Product


def validate_title_length(value):
    # if Product.objects.filter(title__iexact=value).exists():
    #     raise ValidationError('The product title should be unique')
    if len(value) < 5:
        raise ValidationError('Title is too short')
    return value


def validate_title_no_hello(value):
    if "hello" in value.lower():
        raise ValidationError('Hello is not allowed in title')
    return value


unique_product_title = UniqueValidator(queryset=Product.objects.all(),
                                       lookup='iexact')

