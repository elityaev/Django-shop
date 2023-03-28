from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
   CategoriesWithSubcategoriesList,
   ProductViewSet,
   CartView
)

router = DefaultRouter()

router.register('products', ProductViewSet)


urlpatterns = [
   path(
      'categories/', CategoriesWithSubcategoriesList.as_view({'get': 'list'})
   ),
   path('cart/', CartView.as_view()),
   path('', include(router.urls)),
]
