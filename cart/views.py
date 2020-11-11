import json

from django.views   import View
from django.http    import JsonResponse

from .models        import Cart
from utils          import authorization

class CartView(View):
    @authorization
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        try:
            if Cart.objects.filter(user_id = user.id, product_size_id = data['product_size_id']).exists():
                cart = Cart.objects.get(user_id = user.id, product_size_id = data['product_size_id'])
                cart.count += 1
                cart.save()
            else:
                Cart.objects.create(
                    user_id         = user.id,
                    product_id      = data['product_id'],
                    count           = 1,
                    product_size_id = data['product_size_id']
                )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @authorization
    def get(self, request):
            data = [{
                'id'         : cart.product.id,
                'cart_id'    : cart.id,
                'title'      : cart.product.name,
                'count'      : cart.count,
                'price'      : float(cart.product.price),
                'size'       : cart.product_size.size.size,
                'color'      : cart.product.color.first().name,
                'serial_num' : cart.product.serial_number,
                'main_image' : cart.product.main_img_url
                } for cart in Cart.objects.filter(user_id = request.user.id)
                ]
            return JsonResponse({'data' : data}, status = 200)

    @authorization
    def patch(self, request):
        data = json.loads(request.body)

        try:
            if not Cart.objects.filter(id = data['cart_id']).exists():
                return JsonResponse({'message' : 'NOT_EXISTS_CART'}, status = 400)
            
            cart_id          = data['cart_id']
            cart_count       = Cart.objects.get(id = cart_id)
            cart_count.count = int(data['count'])
            cart_count.save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
    @authorization
    def delete(self, request):
        data = json.loads(request.body)
        
        try:
            if not Cart.objects.filter(id = data['cart_id']).exists():
                return JsonResponse({'message' : 'NOT_EXISTS_CART'}, status = 400)

            cart_id    = data['cart_id']
            cart_count = Cart.objects.get(id = cart_id)
            cart_count.delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)