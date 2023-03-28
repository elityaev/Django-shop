from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Product, Cart, CartItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartItemSerializer,
    CartSerializer
)
from .services import (
    get_cart_and_product,
    cart_price_count_update
)


class CategoriesWithSubcategoriesList(viewsets.ReadOnlyModelViewSet):
    """Получить список всех категорий с подкатегориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Получить список всех продуктов."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartView(GenericAPIView):
    """
    Операции с корзиной (доступно только авторизованным
    пользователям и только со своей корзиной).
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get(self, request):
        """
        Возвращает состав корзины текущего пользователя с
        подсчетом количества товаров и суммы стоимости товаров.
        """
        cart = Cart.objects.get(customer=request.user)
        serializer = CartSerializer(cart, context=request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Добавляет новый товар в корзину.
        Query parameters:
        - products: int,
        - count: int
        """
        try:
            _ = request.data['product']
            count = request.data['count']
        except KeyError as error:
            return Response({'message': f'Не передан обязательный аргумент - {error}'})

        cart, product = get_cart_and_product(request)
        request.data['price'] = product.price * count
        request.data['cart'] = cart.id
        serializer = CartItemSerializer(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cart_price_count_update(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        """Изменяет количество товара в корзине

        Query parameters:
        - products: int,
        - count: int (-int при уменьшении количества)

        При передаче в запросе значение count больше чем
        количество товара в корзине, товар удаляется.
        """
        try:
            _ = request.data['product']
            count = request.data['count']
        except KeyError as error:
            return Response({'message': f'Не передан обязательный аргумент - {error}'})

        cart, product = get_cart_and_product(request)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        count = cart_item.count + count
        if count <= 0:
            cart_item.delete()
            cart_price_count_update(cart)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            price = product.price * count
            request.data['price'] = price
            request.data['count'] = count
            serializer = CartItemSerializer(
                cart_item, data=request.data, context=request, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            cart_price_count_update(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """Полная отчистка корзины."""
        cart = Cart.objects.get(customer=request.user.id)
        CartItem.objects.filter(cart=cart).delete()
        cart_price_count_update(cart)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
