import django_filters
from django_filters import Filter
from django_filters.fields import Lookup
from .models import Course,User, Enrolleduser,Category

class EnrollFilter(django_filters.FilterSet):
    userid = django_filters.CharFilter(field_name='userid', label="userid")
    #courseid = django_filters.CharFilter(field_name='courseid', label="courseid")
    courseid = django_filters.ModelChoiceFilter(
        field_name='courseid', queryset=Course.objects.all().values_list('courseid', flat=True).distinct(),
        label="course"
        )
    class Meta:
        model = Enrolleduser
        fields = {"userid","courseid"
        }



class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='iexact',label="Student ID")
    fullname = django_filters.CharFilter(lookup_expr='icontains',label="Full Name")

    class Meta:
        model = Enrolleduser
        fields = {
        }


class CourseFilter(django_filters.FilterSet):
    #categoryname = django_filters.CharFilter(lookup_expr='iexact',label="categoryname")
    categoryname = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all().values_list('categoryname', flat=True).distinct(),
        label="Categoryname"
        )

    class Meta:
        model = Course
        fields = {"categoryname"
        }
class ListFilter(Filter):
    def filter(self, qs, value):

        if  value :
            # print("value is ",value)
            value_list = value.split(u',')
            # print("value is ",value_list)
            self.lookup_expr = 'in'
            return super(ListFilter, self).filter(qs, value_list)
            # return super(ListFilter, self).filter(qs, Lookup(value_list, lookup_expr='in'))
        else:
            # return super(ListFilter, self).filter(qs,value)
            return qs

class UserPriorityFilter(django_filters.FilterSet):
    username = ListFilter(field_name='username')
    # username = django_filters.CharFilter(lookup_expr='iexact',label="Student ID")


    class Meta:
        model = User
        fields = {"priority","username"
        }

class UserSuspendFilter(django_filters.FilterSet):
    username = ListFilter(field_name='username')
    # username = django_filters.CharFilter(lookup_expr='iexact',label="Student ID")


    class Meta:
        model = User
        fields = {"username"
        }
