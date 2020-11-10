from django.db import models

class User(models.Model):
    objects  = models.Manager()
    email    = models.EmailField(unique = True)
    password = models.CharField(max_length = 2000)
    country  = models.CharField(max_length = 200)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
