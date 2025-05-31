from django.db import models

class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        SOLD = 'sold', 'Sold'

    product_id = models.BigAutoField(primary_key=True)
    seller_id = models.BigIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    category_id = models.BigIntegerField()

    def __str__(self):
        return self.title
