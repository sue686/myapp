import django_tables2 as tables
from .models import FileInfo,Category
from django_tables2.utils import A


#
class FileInfoTable(tables.Table):
    class Meta:
        model = FileInfo
        template_name = "django_tables2/semantic.html"
        fields = ("category","filename","uploadtime" )
