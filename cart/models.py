from django.db      import models
from user.models    import User
from product.models import Product, ProductSize

class Cart(models.Model):
    user         = models.ForeignKey(User, on_delete = models.CASCADE)
    product      = models.ForeignKey(Product, on_delete = models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete = models.CASCADE)
    count        = models.IntegerField()

    class Meta:
        db_table = 'carts'