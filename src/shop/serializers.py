from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Subcategory
)


class SubcategorySerializer(serializers.ModelSerializer):
    """Формирует список подкатегорий"""
    class Meta:
        model = Subcategory
        fields = ('name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    """Формирует список категорий с подкатегориями."""
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'image', 'subcategories')


class ProductSerializer(serializers.ModelSerializer):
    """Формирует список продуктов. Для каждого продукта
     в поле images формируется список из 3-х его изображений.
    """
    subcategory = serializers.StringRelatedField()
    category = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'slug', 'category', 'subcategory', 'price', 'images')

    def get_category(self, obj):
        return obj.subcategory.category.name

    def get_images(self, obj):
        request = self.context
        if isinstance(self.context, dict):
            request = self.context['request']
        domain = 'http://' + request.get_host()
        image1 = domain + str(obj.image_one.url)
        image2 = domain + str(obj.image_two.url)
        image3 = domain + str(obj.image_three.url)
        image_list = [image1, image2, image3]
        return image_list


class CartItemProductSerializer(serializers.ModelSerializer):
    """
    Формирует список товаров, находящихся к корзине, с указанием
    количества и общей стоимости конкретного товара.
    """
    product = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('product', 'count', 'price')

    def get_product(self, obj):
        return ProductSerializer(
            Product.objects.filter(
                id=obj.product.id
            ), context=self.context, many=True
        ).data


class CartItemSerializer(serializers.ModelSerializer):
    """
    Формирует данные для добавления нового товара в корзину и
    изменения количества товара, находящегося уже в корзине.
    """
    class Meta:
        model = CartItem
        fields = ('cart', 'product', 'count', 'price')

    def validate(self, data):
        """Предотвращает повторное добавление нового товара в корзину"""
        if self.context.method == 'POST':
            if CartItem.objects.filter(
                    cart=self.initial_data['cart'], product=self.initial_data['product']
            ).exists():
                raise ValidationError(
                    'Этот продукт уже есть в корзине, можно только изменить его количество'
                )
        return data


class CartSerializer(serializers.ModelSerializer):
    """Формирует список товаров, добавленных в корзину
    с подсчетом их общей суммы и количества. Для подробного описания продуктов
    поле products формируется через CartItemProductSerializer."""
    products = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('products', 'total_price', 'total_count')

    def get_products(self, obj):
        return CartItemProductSerializer(
            CartItem.objects.filter(cart=obj), context=self.context, many=True
        ).data
