from django.db import models

# Create your models here.
class Student(models.Model):
    campus =  models.CharField(max_length=120)
    name = models.CharField(max_length=120, unique=True)
    path = models.CharField(max_length=120)
    givenname = models.CharField(max_length=120, blank=True, null=True)
    surname = models.CharField(max_length=120, blank=True, null=True)
    samaccountname = models.CharField(max_length=120)
    displayname = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    email = models.CharField(max_length=120, blank=True, null=True)
    is_in_AD = models.CharField(
        max_length=1, 
        default='n',
        help_text='y means yes, n means no'
    )
    is_in_Elearning = models.CharField(
        max_length=1, 
        default='n',
        help_text='y means yes, n means no'
    )
    createdtime_utc = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.samaccountname
