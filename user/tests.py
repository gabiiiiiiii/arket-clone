import json
import bcrypt
import jwt

from django.test  import TestCase, Client

from .models      import User
from aig.settings import SECRET_KEY, ALGORITHM

client = Client()

class SignUpTest(TestCase):

    def setUp(self):
        User.objects.create(
            email    = 'gabi@gabi.com',
            password = '12345678aA',
            country  = 'South_Korea'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_success(self):
        user = {
            'email'    : 'gabii@gabi.com',
            'password' : '12345678aA',
            'country'  : 'South_Korea'
        }
        response = client.post('/user', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_signup_fail(self):
        user = {
            'email'    : 'gabii@gabi.com',
            'password' : '12345678a',
            'country'  : 'South_Korea'
        }
        response = client.post('/user', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_PASSWORD'})

    def test_signup_duplicate(self):
        user = {
            'email'    : 'gabi@gabi.com',
            'password' : '12345678aA',
            'country'  : 'South_Korea'
        }
        response = client.post('/user', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'EXISTS_EMAIL'})

class SignInTest(TestCase):

    def setUp(self):
        hashed_password = bcrypt.hashpw('12345678aA'.encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(
            email    = 'gabi@gabi.com',
            password = hashed_password.decode('utf-8')
        )
        self.token = jwt.encode({'email':user.email}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')

    def tearDown(self):
        User.objects.all().delete()

    def test_signin_success(self):
        user = {
            'email'    : 'gabi@gabi.com',
            'password' : '12345678aA'
        }
        response = client.post('/user/signin', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'Authorization' : self.token})

    def test_signin_fail(self):
        user = {
            'email'    : 'gabii@gabi.com', 
            'password' : '12345678aA'
        }
        response = client.post('/user/signin', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'INVALID_USER'})