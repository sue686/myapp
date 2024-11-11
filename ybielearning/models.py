from django.db import models

# Create your models here.
PRIORITY_CHOICES = (
    ('priority', 'Priority'),
    ('normal', 'Normal'),
    ('', ''),

)
class User(models.Model):
    userid = models.CharField(max_length=120)
    username = models.CharField(max_length=120,blank=True, null=True)
    firstname = models.CharField(max_length=120,blank=True, null=True)
    lastname = models.CharField(max_length=120,blank=True, null=True)
    fullname = models.CharField(max_length=120,blank=True, null=True)
    email = models.CharField(max_length=120,blank=True, null=True)
    idnumber = models.CharField(max_length=120,blank=True, null=True)
    suspended = models.CharField(max_length=120,blank=True, null=True)
    priority = models.CharField(max_length=120,choices=PRIORITY_CHOICES, blank=True, null=True)

class UserBulk(models.Model):

    username = models.CharField(max_length=120,blank=True, null=True)
    firstname = models.CharField(max_length=120,blank=True, null=True)
    lastname = models.CharField(max_length=120,blank=True, null=True)
    password = models.CharField(max_length=120,blank=True, null=True)
    email = models.CharField(max_length=120,blank=True, null=True)
    createdtime = models.DateTimeField(blank=True, null=True)
    createduser = models.CharField(max_length=120,blank=True, null=True)
    synctime = models.DateTimeField(blank=True, null=True)
    syncuser = models.CharField(max_length=120,blank=True, null=True)
    randomkey = models.CharField(max_length=120,blank=True, null=True)


class Course(models.Model):
    courseid = models.CharField(max_length=120)
    coursename = models.CharField(max_length=120)
    categoryid = models.CharField(max_length=120)
    categoryname = models.CharField(max_length=120,blank=True, null=True)

class Enrolleduser(models.Model):
    courseid = models.CharField(max_length=120,blank=True, null=True)
    userid = models.CharField(max_length=120,blank=True, null=True)
    username = models.CharField(max_length=120,blank=True, null=True)
    fullname = models.CharField(max_length=120,blank=True, null=True)
    roleid = models.CharField(max_length=120,blank=True, null=True)
    rolename = models.CharField(max_length=120,blank=True, null=True)
    suspended = models.CharField(max_length=120,blank=True, null=True)

# class Newenrolluser(models.Model):
#     courseid = models.CharField(max_length=120)
#     userid = models.CharField(max_length=120)
class Category(models.Model):

    categoryid = models.CharField(max_length=120)
    categoryname = models.CharField(max_length=120)

class BBBRecordings(models.Model):
    recordid = models.CharField(max_length=120,blank=True, null=True)
    meetingid = models.CharField(max_length=120,blank=True, null=True)
    name = models.CharField(max_length=120,blank=True, null=True)
    published = models.CharField(max_length=120,blank=True, null=True)
    state = models.CharField(max_length=120,blank=True, null=True)
    starttime = models.CharField(max_length=120,blank=True, null=True)
    endtime = models.CharField(max_length=120,blank=True, null=True)



class BBBbn_logs(models.Model):
    courseid = models.CharField(max_length=120,blank=True, null=True)
    userid = models.CharField(max_length=120,blank=True, null=True)
    bigbluebuttonbnid = models.CharField(max_length=120,blank=True, null=True)
    timecreated = models.CharField(max_length=120,blank=True, null=True)
    meetingid = models.CharField(max_length=120,blank=True, null=True)
    log = models.CharField(max_length=120,blank=True, null=True)
    meta = models.CharField(max_length=800,blank=True, null=True)
