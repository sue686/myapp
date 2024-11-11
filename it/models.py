from django.db import models

# Create your models here.
class Staffbirthday(models.Model):

    name = models.CharField(max_length=120,blank=True, null=True)
    birthdaydate = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)

    adddate = models.DateTimeField(auto_now=True,blank=True, null=True)
