from rest_framework import viewsets, status, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Category, Product, Cart
from .permissions import IsCartOwner, IsCartOwnerForCartItems
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartItemSerializer,
    CartSerializer
)


class CategoriesWithSubcategoriesList(viewsets.ReadOnlyModelViewSet):
    """Получить список всех категорий с подкатегориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Получить список всех продуктов."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Получить состав корзины с общей стоимость и
    количеством продуктов.
    """
    queryset = Cart.objects.all()
    permission_classes = (IsCartOwner,)
    serializer_class = CartSerializer


class CartItemViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Добавить продукт в корзину, изменить количество,
    отчистить корзину полностью.
    """
    serializer_class = CartItemSerializer
    permission_classes = (IsCartOwnerForCartItems,)

    def get_queryset(self):
        cart = get_object_or_404(Cart, id=self.kwargs.get('cart_id'))
        queryset = cart.cart_items.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            cart_id=self.kwargs.get('cart_id')
        )

    def create(self, request, *args, **kwargs):
        request.data['cart'] = self.kwargs.get('cart_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if instance.id is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_queryset()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
