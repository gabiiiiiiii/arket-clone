from django.http      import HttpResponse, JsonResponse
from django.views     import View

from .models          import (MainCategory,
                             SubCategory,
                             Size,
                             Color,
                             Material,
                             Product,
                             ProductMaterial,
                             SubImageUrl,
                             ProductColor,
                             ProductSize)

class ProductView(View):
    def get(self, request, product_id):
        try:
            product         = Product.objects.prefetch_related('material', 'subimageurl_set', 'size', 'productsize_set').\
                              get(id=product_id)
            related_product = Product.objects.prefetch_related('color').filter(name = product.name) 

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=404)

        except:
            return JsonResponse({'message' : 'INVALID_PRODUCT_REQUEST'}, status=404)

        product_dict = {
            "id"            : product.id,
            "Serial_Number" : product.serial_number,
            "Title"         : product.name,
            "Price"         : product.price,
            "Type"          : product.product_type,
            "Material"      : {
                "Material_Img" : product.material.first().image_url,
                "Material_Name": product.material.first().name,
            }
        }

        color_list = [{
            "Color_Name" : related.color.first().name,
            "Color_Img"  : related.main_img_url,
            "Color_Url"  : related.id,
        } for related in related_product]

        size_list = [{
            "Size"    : product.size.all()[i].size,
            "SoldOut" : 'true' if product.productsize_set.all()[i].quantity <= 0 else 'false',
            "ProductSize" : product.productsize_set.all()[i].id,
        } for i in range(len(product.size.all()))]

        image_list = [{
            "Order_Num" : image.display_order,
            "Img_Url"   : image.image_url,
        } for image in product.subimageurl_set.all()]

        product_detail = {
            'product'     : product_dict,
            'Color'       : color_list,
            'ProductSize' : size_list,
            'Images'      : image_list,
        }

        return JsonResponse({'data': product_detail}, status = 200)

class ProductsView(View):
    def get(self, request):
        try:
            color_id    = request.GET.getlist('color', None)
            material_id = request.GET.getlist('material', None)
            category_id = request.GET.get('category',None)
            
            products = Product.objects.prefetch_related('color', 'material').select_related('sub_category').all()
            products = products.filter(sub_category_id = category_id) if category_id else products
            products = products.filter(color__in = color_id) if color_id else products
            products = products.filter(material__in = material_id) if material_id else products

        except:
            return JsonResponse({'message' : 'INVALID_PRODUCT_REQUEST'}, status=404)

        product_list = [{
                'itemCategory' : product.sub_category_id,
                'itemName'     : product.name,
                'itemPrice'    : product.price,
                'itemImage'    : product.main_img_url,
                'itemId'       : product.id,
        } for product in products]

        return JsonResponse({'data': product_list, 'count' : Product.objects.count()}, status = 200)
