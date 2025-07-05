from django.conf import settings
from django.db import models

class Product(models.Model):
    title       = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    image_url   = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    is_paid     = models.BooleanField(default=False)

    def __str__(self):
        return f'Order #{self.pk} by {self.user}'

class OrderItem(models.Model):
    order   = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity
