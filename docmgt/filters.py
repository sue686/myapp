import django_filters
from django_filters import Filter
from django_filters.fields import Lookup
from docmgt.models import FileInfo,Category
from django.contrib.auth.models import Group

class FileFilter(django_filters.FilterSet):

    def categoryqs(request):

        campus = request.get_full_path().split("/")[3]
        department = request.get_full_path().split("/")[4]
        # categoryids = request.get_full_path().split("/")[5]
        # print(categoryids)
        groupids = request.user.groups.values_list('id', flat=True)
        permissions = Category.objects.all().values('permission','id')
        categoryids = []

        # Enrolleduser.objects.all().delete()
        # #for id in [{'courseid': '107'}]:
        for groupiditem in groupids:
            groupid = groupiditem

            for permissionitem in permissions:
                permission = permissionitem["permission"]
                # print(permission)
                # print("groupid is ",groupid)

                if permission:

                    permission=permission.split(",")
                    for i in range(0, len(permission)):

                        permission[i] = int(permission[i])
                    if groupid in permission:

                        if not permissionitem["id"] in categoryids:

                            categoryids.append(permissionitem["id"])



        return Category.objects.filter(campus=campus,department=department,pk__in = categoryids)

    category = django_filters.ModelChoiceFilter(queryset=categoryqs,label='Category')
    filename = django_filters.CharFilter(lookup_expr='icontains',label="Filename")


    class Meta:
        model = FileInfo
        fields = {'category','filename'}
        sequence  = ('category','filename')
