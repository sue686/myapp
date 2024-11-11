import django_filters
from django_filters import Filter
from django_filters.fields import Lookup
from .models import Staffbirthday



class BirthdayFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains',label="NAME")


    class Meta:
        model = Staffbirthday
        fields = {
        }
