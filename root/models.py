from django.db import models

# Create your models here.


class Wishlist(models.Model):
    name = models.CharField(max_length=140)
    product = models.CharField(max_length=140, default="not specified")
    imageurl = models.CharField(max_length=140, default="not specified")
    title=models.CharField(max_length=140, default="not specified")
    
    def __str__(self):
        return self.name
