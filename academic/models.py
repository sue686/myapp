from django.db import models

# Create your models here.


TERM_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)

YEAR_CHOICES = (
    ('2020', '2020'),
    ('2021', '2021'),
    ('2022', '2022'),
    ('2023', '2023'),
)
CAMPUS_CHOICES = (
    ('ybi', 'ybi'),
    ('bbi', 'bbi'),

)
class AcademicCalendar(models.Model):
    year = models.CharField(max_length=120,choices=YEAR_CHOICES,)
    term = models.CharField(max_length=120,choices=TERM_CHOICES, blank=True, null=True)
    startdate = models.DateTimeField(blank=True, null=True)
    finishdate = models.DateTimeField(blank=True, null=True)
    intakedate = models.DateTimeField(blank=True, null=True)
    campus = models.CharField(max_length=120,choices=CAMPUS_CHOICES,blank=True, null=True)
    def __str__(self):
        return self.year
