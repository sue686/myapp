from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
# Create your models here.


class Department(models.Model):

    departmentname = models.CharField(max_length=120)

    def __str__(self):
        return self.departmentname



class UserProfile(models.Model):



    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')

    department = models.ForeignKey(Department,on_delete=models.CASCADE)

    image = models.ImageField(default='default.jpg',upload_to="profilepics")

    def __str__(self):
        return str(self.user)

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300 ,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class EmailGroup(models.Model):

    groupname = models.CharField(max_length=120)


    def __str__(self):
        return self.groupname

class EmailAddress(models.Model):

    groupname = models.ForeignKey(EmailGroup,on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email
