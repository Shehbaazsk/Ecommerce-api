from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.api.api_views import CategoryAPIViewSet, SubCategoryAPIViewSet, ProductAPIViewSet

app_name = 'prodcuts'

router = DefaultRouter()
router.register('category',CategoryAPIViewSet,basename='category')
router.register('sub_category',SubCategoryAPIViewSet,basename='sub_category')
router.register('products',ProductAPIViewSet,basename='products')


urlpatterns = [
    path('', include(router.urls)),
]
