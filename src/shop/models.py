from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Category(models.Model):
    """Модель для категорий."""
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    image = models.ImageField(upload_to='images/categories/')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Модель для подкатегорий."""
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    image = models.ImageField(upload_to='images/subcategories/')
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель для продуктов."""
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
    image_one = models.ImageField(upload_to='images/products/')
    image_two = models.ImageField(upload_to='images/products/')
    image_three = models.ImageField(upload_to='images/products/')

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Модель для корзины."""
    customer = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_count = models.IntegerField(default=0)


class CartItem(models.Model):
    """Модель, связывающая корзину с продуктами."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)


@receiver(post_save, sender=User)
def get_cart_price(sender, **kwargs):
    """Создает корзину пользователя при его аутентификации."""
    user = kwargs['instance']
    cart = Cart.objects.create(customer=user)
    cart.save()
