from django.db   import models
from user.models import User

class Review(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    email       = models.CharField(max_length=50)
    grade       = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    title       = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    img_url     = models.URLField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'reviews'
