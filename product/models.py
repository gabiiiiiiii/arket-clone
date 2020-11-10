from django.db import models

class MainCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'main_categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name     = models.CharField(max_length=50)
    category = models.ForeignKey(MainCategory,on_delete = models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

    def __str__(self):
        return self.name

class Size(models.Model):
    size = models.CharField(max_length=50)

    class Meta:
        db_table = 'sizes'

    def __str__(self):
        return self.size

class Color(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'colors'
    
    def __str__(self):
        return self.name

class Material(models.Model):
    name      = models.CharField(max_length=50)
    image_url = models.URLField()

    class Meta:
        db_table = 'materials'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name          = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    product_type  = models.CharField(max_length=50)
    price         = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    main_img_url  = models.URLField()
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    sub_category  = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    size          = models.ManyToManyField(Size, through = 'ProductSize')
    color         = models.ManyToManyField(Color, through = 'ProductColor') 
    material      = models.ManyToManyField(Material, through = 'ProductMaterial') 
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name

class ProductMaterial(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_materials'

class SubImageUrl(models.Model):
    image_url     = models.URLField()
    display_order = models.IntegerField()
    product       = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_image_urls'

class ProductColor(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    color    = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_colors'
    
class ProductSize(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    size     = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'products_sizes'

