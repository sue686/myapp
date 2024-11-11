from django.db import models

# Create your models here.
class Category(models.Model):
    categoryname = models.CharField(max_length=120)
    department = models.CharField(max_length=120,blank=True, null=True)
    campus = models.CharField(max_length=120,blank=True, null=True)
    permission = models.CharField(max_length=120,blank=True, null=True)
    permissionname = models.CharField(max_length=520,blank=True, null=True)
    createtime = models.DateTimeField(max_length=120,blank=True, null=True)
    createuser = models.CharField(max_length=120,blank=True, null=True)
    lastupdatetime = models.DateTimeField(blank=True, null=True)
    lastupdateuser = models.CharField(max_length=120,blank=True, null=True)

    def __str__(self):
        return self.categoryname

class FileInfo(models.Model):
    filename = models.CharField(max_length=120)
    filesize = models.DecimalField(max_digits=10, decimal_places=0)
    filepath = models.CharField(max_length=120,blank=True, null=True)
    uploadtime = models.DateTimeField(blank=True, null=True)
    uploaduser = models.CharField(max_length=120,blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    department = models.CharField(max_length=120,blank=True, null=True)
    campus = models.CharField(max_length=120,blank=True, null=True)
