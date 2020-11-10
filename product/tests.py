import json

from django.test import TestCase, Client
from .models     import (MainCategory,
                        SubCategory,
                        Size,
                        Color,
                        Material,
                        Product,
                        ProductMaterial,
                        SubImageUrl,
                        ProductColor,
                        ProductSize)

def create_data():
    size_list = ['S', 'M', 'L', 'XL']
    main_category = MainCategory.objects.create(
        name = '테스트 메인 카테고리',
    )

    sub_category = SubCategory.objects.create(
        name        = '테스트 서브 카테고리',
        category    = MainCategory.objects.first(),
    )

    Size.objects.bulk_create(
        [Size(id = 1, size = size_list[0]),
         Size(id = 2, size = size_list[1]),
         Size(id = 3, size = size_list[2]),
         Size(id = 4, size = size_list[3])]
    )

    color = Color.objects.create(
        id   = 1,
        name = '테스트 컬러',
    )

    material = Material.objects.create(
        id        = 1,
        name      = '테스트 재료',
        image_url = '테스트 이미지',
    )

    product = Product.objects.create(
        id            = 1,
        name          = '테스트 상품',
        serial_number = '테스트 시리얼넘버',
        product_type  = '테스트 상품타입',
        price         = 999,
        main_img_url  = '테스트 이미지',
        main_category = main_category,
        sub_category  = sub_category,
    )

    product_material = ProductMaterial.objects.create(
        product  = product,
        material = material,
    )

    sub_img_url = SubImageUrl.objects.create(
        image_url     = '테스트 이미지',
        display_order = 1,
        product    = product,
    )
    
    product_color = ProductColor.objects.create(
        product  = product,
        color    = color,
    )

    ProductSize.objects.bulk_create(
        [ProductSize(id = 1, product = Product.objects.first(), size = Size.objects.get(size=size_list[0]), quantity = 10),
         ProductSize(id = 2, product = Product.objects.first(), size = Size.objects.get(size=size_list[1]), quantity = 10),
         ProductSize(id = 3, product = Product.objects.first(), size = Size.objects.get(size=size_list[2]), quantity = 10),
         ProductSize(id = 4, product = Product.objects.first(), size = Size.objects.get(size=size_list[3]), quantity = 10)]
    )

def delete_data():
    MainCategory.objects.all().delete()
    SubCategory.objects.all().delete()
    Size.objects.all().delete()
    Color.objects.all().delete()
    Material.objects.all().delete()
    Product.objects.all().delete()
    ProductMaterial.objects.all().delete()
    SubImageUrl.objects.all().delete()
    ProductColor.objects.all().delete()
    ProductSize.objects.all().delete()

class ProductDetailTest(TestCase):
    maxDiff = None
    def setUp(self):
        client = Client()
        create_data()

    def tearDown(self):
        delete_data()    

    def test_detail_get_success(self):
        response = self.client.get(f'/products/{Product.objects.first().id}')
        self.assertEqual(response.json(), {
            "data": {
                "product": {
                    "id"            : 1,
                    "Serial_Number" : "테스트 시리얼넘버",
                    "Title"         : "테스트 상품",
                    "Price"         : "999",
                    "Type"          : "테스트 상품타입",
                    "Material"      : {
                        "Material_Img" : "테스트 이미지",
                        "Material_Name": "테스트 재료"
                    }
                },
                "Color": [
                    {
                        "Color_Name": "테스트 컬러",
                        "Color_Img" : "테스트 이미지",
                        "Color_Url" : 1
                    }
                ],
                "ProductSize": [
                    {
                        "Size"   : "S",
                        "SoldOut": "false",
                        "ProductSize" : 1
                    },
                    {
                        "Size"   : "M",
                        "SoldOut": "false",
                        "ProductSize" : 2
                    },
                    {
                        "Size"   : "L",
                        "SoldOut": "false",
                        "ProductSize" : 3
                    },
                    {
                        "Size"   : "XL",
                        "SoldOut": "false",
                        "ProductSize" : 4
                    }
                ],
                "Images": [
                    {
                        "Order_Num": 1,
                        "Img_Url"  : "테스트 이미지"
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 200)

    def test_detail_get_fail(self):
        response = self.client.get('/product/1')
        self.assertEqual(response.status_code, 404)

    def test_detail_get_except(self):
        response = self.client.get('/products/2')
        self.assertEqual(response.json(),{'message': 'PRODUCT_DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 404)

class ProductListTest(TestCase):
    maxDiff = None
    
    def setUp(self):
        client = Client()
        create_data()

    def tearDown(self):
        delete_data() 

    def test_products_get_success(self):
        response = self.client.get('/products')
        self.assertEqual(response.json(), {
            "count" : 1,
            "data" : [
                {
                    "itemId": 1,
                    "itemImage": "테스트 이미지",
                    "itemName": "테스트 상품",
                    "itemPrice": "999",
                }
            ]
        })
        self.assertEqual(response.status_code, 200)

    def test_products_get_fail(self):
        response = self.client.get('/product')
        self.assertEqual(response.status_code, 404)

    def test_products_get_except(self):
        response = self.client.get('/products/200')
        self.assertEqual(response.json(),{'message': 'PRODUCT_DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 404)

    def test_products_filterling_color(self):
        response = self.client.get('/products?color=1')
        self.assertEqual(response.json(), {
            "count" : 1,
            "data" : [
                {
                    "itemId": 1,
                    "itemImage": "테스트 이미지",
                    "itemName": "테스트 상품",
                    "itemPrice": "999",
                }
            ]
        })
        self.assertEqual(response.status_code, 200)

    def test_products_filterling_material(self):
        response = self.client.get('/products?material=1')
        self.assertEqual(response.json(), {
            "count" : 1,
            "data" : [
                {
                    "itemId": 1,
                    "itemImage": "테스트 이미지",
                    "itemName": "테스트 상품",
                    "itemPrice": "999",
                }
            ]
        })
        self.assertEqual(response.status_code, 200)

    def test_products_filtering_with_color_and_material(self):
        response = self.client.get('/products?color=1&material=1')
        self.assertEqual(response.json(), {
            "count" : 1,
            "data" : [
                {
                    "itemId": 1,
                    "itemImage": "테스트 이미지",
                    "itemName": "테스트 상품",
                    "itemPrice": "999",
                }
            ]
        })
        self.assertEqual(response.status_code, 200)
