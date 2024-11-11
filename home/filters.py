import django_filters
from django_filters import Filter
from django_filters.fields import Lookup
from docmgt.models import FileInfo
from blog.models import Post
from academic.models import AcademicCalendar

class PostFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains',label="Title")

    class Meta:
        model = Post
        fields = {'title'
        }

class FileFilter(django_filters.FilterSet):

    filename = django_filters.CharFilter(lookup_expr='icontains',label="Filename")

    class Meta:
        model = FileInfo
        fields = {'filename'
        }

class AcademicCalendarFilter(django_filters.FilterSet):

    year = django_filters.CharFilter(lookup_expr='icontains',label="Year")

    class Meta:
        model = AcademicCalendar
        fields = {'year'
        }
