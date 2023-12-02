from django.db import models

# Create your models here.

class Tokens(models.Model):
    token = models.CharField(max_length=7)
    status = models.CharField(max_length=50)
    table = models.CharField(max_length=10)
    def __str__(self):
        return self.token
class Menu(models.Model):
    category = models.CharField(max_length=50)
    item = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    def __str__(self):
        return self.item
class Current_Orders(models.Model):
    token = models.CharField(max_length=10)
    items = models.CharField(max_length=1000)
    table = models.CharField(max_length=20)
    def __str__(self):
        return self.table

class Completed_Orders(models.Model):
    token = models.CharField(max_length=10)
    items = models.CharField(max_length=1000)
    paymentmode = models.CharField(max_length=20)
    total_payment = models.CharField(max_length=20)
    date = models.CharField(max_length=30)
    def __str__(self):
        return self.token