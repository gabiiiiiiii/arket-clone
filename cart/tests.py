import json
import bcrypt
import jwt

from django.views   import View
from django.test    import TestCase, Client
from django.http    import JsonResponse

from aig.settings   import SECRET_KEY, ALGORITHM
from .models        import Cart
from user.models    import User
from product.models import (Product, 
                            ProductSize, 
                            MainCategory, 
                            SubCategory,
                            Size,
                            Color,
                            ProductColor)
from utils          import authorization

client = Client()

class CartTest(TestCase):

    def setUp(self):

        user = User.objects.create(
            id       = 1,
            email    = 'gabi@gabi.com',
            password = '12345678aA'
        )
        print(user.id)
        main_category = MainCategory.objects.create(
            id   = 1,
            name = 'WOMEN'
        )
       

        sub_category = SubCategory.objects.create(
            id   = 1,
            name = 'Blazers',
            category_id = main_category.id
        )

        product = Product.objects.create(
            id               = 1,
            name             = 'Crown Clown Dress',
            serial_number    = '0596182-002',
            product_type     = 'Dresses',
            price            = 129,
            main_img_url     = 'https://github.com/dobidoggy/web1/blob/master/1-1.jpg?raw=true',
            main_category_id = main_category.id,
            sub_category_id  = sub_category.id
        )

        size = Size.objects.create(
            id   = 1,
            size = 'S'
        )

        product_size = ProductSize.objects.create(
            id         = 1,
            quantity   = 1,
            product_id = product.id,
            size_id    = size.id
        )

        cart = Cart.objects.create(
            id              = 1,
            user_id         = user.id,
            product_id      = product.id,
            product_size_id = product_size.id,
            count           = 1,
        )

        color = Color.objects.create(
            id   = 1,
            name = 'White'
        )

        ProductColor.objects.create(
            color_id   = color.id,
            product_id = product.id 
        )

        self.token = jwt.encode({'email':user.email}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')

        headers = {'HTTP_Authorization' : self.token}

        
    def tearDown(self):
        Cart.objects.all().delete()
        User.objects.all().delete()
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        Size.objects.all().delete()
        ProductSize.objects.all().delete()

    def test_cart_post_success(self):
        headers = {'HTTP_Authorization' : self.token}

        cart = {
            'user_id'         : 1,
            'product_id'      : 1,
            'product_size_id' : 1,
            'count'           : 1
        }
        
        response = client.post('/cart', json.dumps(cart), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message' : 'SUCCESS'})

    def test_cart_post_fail(self):
        headers = {'HTTP_Authorization' : self.token}

        cart = {
            'user_id'    : 1,
            'product_id' : 1,
            'count'      : 1
        }
        response = client.post('/cart', json.dumps(cart), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})

    def test_cart_get_success(self):
        headers = {'HTTP_Authorization' : self.token}
        data = [{
                'id'         : cart.product.id,
                'cart_id'    : cart.id,
                'title'      : cart.product.name,
                'count'      : cart.count,
                'price'      : cart.product.price,
                'size'       : cart.product_size.size.size,
                'color'      : cart.product.color.first().name,
                'serial_num' : cart.product.serial_number,
                'main_image' : cart.product.main_img_url
                } for cart in Cart.objects.filter(user_id = 1)
                ]

        response = client.get('/cart', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data' : data})

    def test_cart_patch_success(self):
        headers = {'HTTP_Authorization' : self.token}
        
        cart = {
            'cart_id' : 1,
            'count'   : 1
        }

        response = client.patch('/cart', json.dumps(cart), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_cart_patch_not_exists(self):
        headers = {'HTTP_Authorization' : self.token}

        cart = {
            'cart_id' : 2,
            'count'   : 1
        }

        response = client.patch('/cart', json.dumps(cart), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_EXISTS_CART'})

    def test_cart_patch_fail(self):
        headers = {'HTTP_Authorization' : self.token}

        cart = {
            'count'   : 1
        }

        response = client.patch('/cart', json.dumps(cart), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})

    def test_cart_delete_success(self):
        headers = {'HTTP_Authorization' : self.token}

        cart = {
            'cart_id' : 1
        }

        response = client.delete('/cart', json.dumps(cart), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_cart_delete_not_exists(self):
        headers = {'HTTP_Authorization' : self.token}

        cart = {
            'cart_id' : 2
        }

        response = client.delete('/cart', json.dumps(cart), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_EXISTS_CART'})

    def test_cart_delete_fail(self):
        headers = {'HTTP_Authorization' : self.token}

        cart = {
            'cart' : 2
        }

        response = client.delete('/cart', json.dumps(cart), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})