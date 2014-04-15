from django.db import models

# Create your models here.
class Record(models.Model):
    company = models.CharField(max_length=200)
    phone = models.IntegerField()
    price   = models.FloatField()
    duration = models.IntegerField()