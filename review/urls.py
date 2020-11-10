from django.urls import path
from .views      import *

urlpatterns = [
    path('/<int:review_id>',ReviewsView.as_view()),
    path('',ReviewsView.as_view()),
]
