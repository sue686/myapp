import django_filters
from django_filters import Filter
from django_filters.fields import Lookup
from .models import Post

class PostFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains',label="Title")

    class Meta:
        model = Post
        fields = {'title'
        }
