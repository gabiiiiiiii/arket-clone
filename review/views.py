import bcrypt, json, jwt
import datetime

from django.http    import HttpResponse, JsonResponse
from django.views   import View

from .models        import Review
from user.models    import User

from utils          import authorization
from aig.settings   import SECRET_KEY, ALGORITHM

class ReviewsView(View):
    @authorization
    def post(self, request):
        try:
            data          = json.loads(request.body)

            review = Review.objects.create(
                user_id     = request.user.id, 
                email       = request.user.email,  
                grade       = int(data['grade']),
                title       = data['title'],
                description = data['description'],
                img_url     = data['imageUrl'], 
            )

            reviews     = Review.objects.select_related('user').order_by('-id').all()
            review_list = [{
                "reviewId"       : review.id,
                "email"          : review.email,
                "grade"          : int(review.grade),
                "title"          : review.title,
                "description"    : review.description,
                "imageUrl"       : review.img_url,
                "date"           : review.created_at,
                "isLoggedInUser" : True if review.user.id == request.user.id else False,
                "isEditing"      : False
            } for review in reviews]

            return JsonResponse({'data': review_list}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

    def get(self, request):
        try:
            access_token = request.headers.get("Authorization", None)
            reviews      = Review.objects.select_related('user').order_by('-id').all()
            
            if access_token:
                token_paylod  = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
                request.user  = User.objects.get(email = token_paylod['email'])
                review_list = [{
                    "reviewId"       : review.id,
                    "email"          : review.email,
                    "grade"          : int(review.grade),
                    "title"          : review.title,
                    "description"    : review.description,
                    "imageUrl"       : review.img_url,
                    "date"           : review.created_at,
                    "isLoggedInUser" : True if review.user.id == request.user.id else False,
                    "isEditing"      : False
                } for review in reviews]
            else:
                review_list = [{
                    "reviewId"       : review.id,
                    "email"          : review.email,
                    "grade"          : int(review.grade),
                    "title"          : review.title,
                    "description"    : review.description,
                    "imageUrl"       : review.img_url,
                    "date"           : review.created_at,
                    "isLoggedInUser" : False
                } for review in reviews]
            
            return JsonResponse({'data': review_list}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

    @authorization
    def patch(self, request):
        try:
            data          = json.loads(request.body)
            review_id     = data['reviewId']
        
            updated_review             = Review.objects.get(id=review_id) 
            updated_review.title       = data['title'] 
            updated_review.description = data['description']
            updated_review.save()

            reviews     = Review.objects.select_related('user').order_by('-id').all()
            review_list = [{
                "reviewId"       : review.id,
                "email"          : review.email,
                "grade"          : int(review.grade),
                "title"          : review.title,
                "description"    : review.description,
                "imageUrl"       : review.img_url,
                "date"           : review.created_at,
                "isLoggedInUser" : True if review.user.id == request.user.id else False,
                "isEditing"      : False
            } for review in reviews]

            return JsonResponse({'data': review_list}, status=200)
            
        except Review.DoesNotExist:
            return JsonResponse({'message':'DOES_NOT_EXIST'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @authorization
    def delete(self, request, review_id):
        try:
            Review.objects.get(id = review_id).delete()
            reviews     = Review.objects.select_related('user').order_by('-id').all()
            review_list = [{
                "reviewId"       : review.id,
                "email"          : review.email,
                "grade"          : int(review.grade),
                "title"          : review.title,
                "description"    : review.description,
                "imageUrl"       : review.img_url,
                "date"           : review.created_at,
                "isLoggedInUser" : True if review.user.id == request.user.id else False,
                "isEditing"      : False
            } for review in reviews]

            return JsonResponse({'data': review_list}, status=200)

        except Review.DoesNotExist:
            return JsonResponse({'message':'DOES_NOT_EXIST'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

