from django.contrib import admin
from .models import AcademicCalendar
# Register your models here.



class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('year','term','startdate','finishdate','intakedate')

admin.site.register(AcademicCalendar,AcademicCalendarAdmin)
