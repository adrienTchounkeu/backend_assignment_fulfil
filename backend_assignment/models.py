from django.db import models


# basic user schema
class User(models.Model):
    name = models.CharField(max_length=500)
    create_trigger = models.BooleanField(default=False)
    update_trigger = models.BooleanField(default=False)


# product schema
class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=500)
    status = models.BooleanField(default=False)
