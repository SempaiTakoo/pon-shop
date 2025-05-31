from django.http import JsonResponse
from django.views import View
import json
from .services import ProductService

class ProductView(View):
    def get(self, request, product_id=None):
        if product_id:
            product = ProductService.get_product(product_id)
            return JsonResponse(model_to_dict(product))
        else:
            products = ProductService.list_products()
            return JsonResponse([model_to_dict(p) for p in products], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        product = ProductService.create_product(data)
        return JsonResponse(model_to_dict(product), status=201)

    def put(self, request, product_id):
        data = json.loads(request.body)
        product = ProductService.update_product(product_id, data)
        return JsonResponse(model_to_dict(product))

    def delete(self, request, product_id):
        ProductService.delete_product(product_id)
        return JsonResponse({'status': 'deleted'}, status=204)
