from django.db import models


class BBBRecordingsView(models.Model):
    id = models.CharField(max_length=120,primary_key=True)
    recordid = models.CharField(max_length=120,blank=True, null=True)
    meetingid = models.CharField(max_length=120,blank=True, null=True)
    name = models.CharField(max_length=120,blank=True, null=True)
    published = models.CharField(max_length=120,blank=True, null=True)
    state = models.CharField(max_length=120,blank=True, null=True)
    starttime = models.CharField(max_length=120,blank=True, null=True)
    endtime = models.CharField(max_length=120,blank=True, null=True)
    courseid = models.CharField(max_length=120,blank=True, null=True)
    coursename = models.CharField(max_length=120,blank=True, null=True)
    categoryid = models.CharField(max_length=120,blank=True, null=True)
    categoryname = models.CharField(max_length=120,blank=True, null=True)




    class Meta:
        db_table = 'bbielearning_bbbrecordings_view'
