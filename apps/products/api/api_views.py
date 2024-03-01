from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from products.serializers import CategorySerializer, SubCategorySerializer, ProductSerializer
from products.models import Category, SubCategory, Product

class CategoryAPIViewSet(ReadOnlyModelViewSet):
    """"Category Read Only ModelViewSet"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryAPIViewSet(ReadOnlyModelViewSet):
    """"Sub-Category Read Only ModelViewSet"""

    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class ProductAPIViewSet(ReadOnlyModelViewSet):
    """"Product Read Only ModelViewSet"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['name','description']
    filterset_fileds = ['sub_category__category','price']
    ordering_fields = ['price','name']
