from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Record(models.Model):
    """
    id: the primary key
    name: the company's name
    telnum: telephone number of the company
    type: 0 - fixed price by month
          1 - fixed price by year
          2 - fixed price through a given date
          3 - monthly variable price
    month: for type 0
    year: for type 1
    date: for type 2
    price: price in cents per month
    fee: extra fee
    annotation: extra information
    """
    name = models.CharField(max_length=50)
    telnum = models.CharField(max_length=15, null=True)
    type = models.IntegerField( null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    date = models.DateField(null=True)
    price   = models.FloatField(null=True)
    fee = models.IntegerField(null=True)
    annotation = models.CharField(max_length=500, null=True)
    
    
    def __str__( self ):
        return self.name
    
    
class Query( models.Model ):
    user = models.ForeignKey(User)
    queryStr = models.CharField(max_length=200)
    queryRes = models.ManyToManyField(Record)
    cntRes = models.IntegerField( null=True )
    isRegistered = models.BooleanField(default=False)
    time = models.DateTimeField( auto_now=True )
    
    
    def __str__( self ):
        return self.queryStr