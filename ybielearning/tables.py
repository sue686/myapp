import django_tables2 as tables
from .models import Course,User, Enrolleduser,UserBulk
from django_tables2.utils import A


#
class CoursesTable(tables.Table):
    class Meta:
        model = Course
        template_name = "django_tables2/bootstrap4.html"
        fields = ("courseid","coursename","categoryname" )


class UsersTable(tables.Table):
    #  selected = tables.CheckBoxColumn(accessor="pk")
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields = ("userid","username","fullname" ,"suspended")


class EnrolledusersTable(tables.Table):
    class Meta:
        model = Enrolleduser
        template_name = "django_tables2/semantic.html"
        fields = ("courseid","userid","username" ,"fullname","suspended")

class UserBulkTable(tables.Table):
    class Meta:
        model = UserBulk
        template_name = "django_tables2/semantic.html"
        fields = ("username","firstname","lastname" ,"password","email")

class UsersPriorityTable(tables.Table):
    selected = tables.CheckBoxColumn(accessor="pk",attrs={"th__input": {"id": "all"}})
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields  = ("selected","username","fullname","priority")
        sequence  = ("selected","username","fullname","priority")
        
class UsersSuspendTable(tables.Table):
    selected = tables.CheckBoxColumn(accessor="pk",attrs={"th__input": {"id": "all"}})
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields  = ("selected","username","fullname","suspended")
        sequence  = ("selected","username","fullname","suspended")
