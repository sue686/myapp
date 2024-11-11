import django_tables2 as tables
from .models import Staffbirthday
from django_tables2.utils import A


#
class BirthdayTable(tables.Table):
    class Meta:
        model = Staffbirthday
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name","birthdaydate","adddate")
