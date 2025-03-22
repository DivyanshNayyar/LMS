from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
import os
from django.utils import timezone

import datetime

from django.db.models.deletion import CASCADE

# model for products
# model for otp 
# model for transactions
# model for saved cards

class cards(models.Model):
    name = models.CharField(max_length=100, null= False, blank = False)
    cardnumber = models.IntegerField(null=False, blank=False)
    email = models.EmailField(default = "parvg555@gmail.com",null=False,blank=False)
    cvv = models.IntegerField(null=False, blank=False)
    expYear = models.IntegerField(null=False,blank=False)
    expMonth = models.IntegerField(null = False, blank=False)
    highamount = models.IntegerField(null=False,blank = False) 
    securityquestion = models.CharField(default = "null",max_length=100, null=False,blank=False)
    securityans = models.CharField(default="null",max_length=100, null=False,blank=False)

    def __str__(self):
        return str(self.cardnumber)

class product(models.Model):
    name = models.CharField(max_length = 100,null = False, blank = False)
    image = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT))
    quantity = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name

class Otp(models.Model):
    cardnumber = models.IntegerField(default = 0,null=False, blank=False)
    code = models.IntegerField(null=False, blank=False)
    Expire_time = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(minutes = 5),blank=False)

    def __str__(self):
        return str(self.cardnumber) + str(self.code)

    @property
    def deleteafterfiveminutes(self):
        if self.Expire_time < datetime.datetime.now():
            e = Otp.objects.get(id=self.id)
            e.delete()
            return True
        else:
            return False


class Trasaction(models.Model):
    product = models.ForeignKey(product,on_delete = models.CASCADE)
    ip = models.CharField(max_length = 16, null=False, blank=False)
    card = models.ForeignKey(cards, on_delete= models.CASCADE,null=True, blank=True)

    def __str__(self):
        return str(self.product.name) + str(self.ip)


