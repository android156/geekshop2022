from django.db import models

from users.models import User
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def amount_basket_items(self):
        baskets = Basket.objects.filter(user=self.user).select_related('product')
        return sum(basket.quantity for basket in baskets)

    def total_price(self):
        baskets = Basket.objects.filter(user=self.user).select_related('product')
        return sum(basket.sum() for basket in baskets)

    def get_items(current_user):
        return Basket.objects.filter(user=current_user)
