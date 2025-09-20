
# Create your models here.
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # image = models.ImageField(upload_to='books/', blank=True, null=True, default='books/default.png')


    def __str__(self):
        return self.title