from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    content = RichTextUploadingField()
    department = models.CharField(max_length=120)
    campus = models.CharField(max_length=120,blank=True, null=True)
    top = models.BooleanField(default=False)
    email = models.BooleanField(default=True)
    postdate = models.DateTimeField(blank=True, null=True)
    postuser = models.CharField(max_length=120,blank=True, null=True)
    updatedate = models.DateTimeField(blank=True, null=True)
    updateuser = models.CharField(max_length=120,blank=True, null=True)

    def __str__(self):
        return self.title
