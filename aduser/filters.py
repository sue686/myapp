import django_filters
from django_filters import Filter
from django_filters.fields import Lookup
from .models import Student

class StudentFilter(django_filters.FilterSet):

    samaccountname = django_filters.CharFilter(
        field_name='samaccountname', 
        label="Student ID",
        lookup_expr='icontains'  # This allows partial matching, case-insensitive
    )

    class Meta:
        model = Student
        fields = {'samaccountname'
        }
