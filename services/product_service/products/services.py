from .models import Product
from django.shortcuts import get_object_or_404

class ProductService:
    @staticmethod
    def create_product(data):
        return Product.objects.create(**data)

    @staticmethod
    def get_product(product_id):
        return get_object_or_404(Product, pk=product_id)

    @staticmethod
    def update_product(product_id, data):
        product = get_object_or_404(Product, pk=product_id)
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def delete_product(product_id):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return True

    @staticmethod
    def list_products():
        return Product.objects.all()
