from django.db.models import Sum

from .models import CartItem, Cart, Product


def cart_price_count_update(cart):
    """Обновляет общую стоимость и количество товаров в корзине."""
    result = CartItem.objects.filter(cart=cart).aggregate(
        total_price=Sum('price'), total_count=Sum('count'))
    cart.total_price = result['total_price']
    cart.total_count = result['total_count']
    if not result['total_count'] and not result['total_price']:
        cart.total_price = 0
        cart.total_count = 0
    cart.save()


def get_cart_and_product(request):
    """
    Возвращает корзину текущего пользователя
    и объект Product, полученный в запросе.
    """
    cart = Cart.objects.get(customer=request.user.id)
    product = Product.objects.get(id=request.data.get('product'))
    return cart, product
