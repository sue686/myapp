from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.http import FileResponse
from django.template import RequestContext
from django.urls import reverse
from urllib.parse import quote


from home.models import UserProfile
from .models import FileInfo,Category
from home.models import Department
from home.views import paginate
from .forms import UploadForm,CategoryForm,CategoryUpdateForm,ViewForm
import os
from .tables import FileInfoTable
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from .filters import FileFilter
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
import random


def param(campus,department):
    base_template="home/" + campus +"base.html"
    if campus == "weg":
        urlhome = "home"
    else:
        urlhome = campus + "home"
    return base_template,urlhome


@login_required
def doclist(request,campus,department,pagenumber):

    base_template,urlhome=param(campus,department)



    # form = UploadForm()
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






    documentfilter = FileFilter(request.GET,request=request,queryset=FileInfo.objects.filter(campus=campus,department=department,category_id__in = categoryids).order_by('category', 'filename'))
    paginator,current_page,is_paginated,Items = paginate(documentfilter.qs,request,25,pagenumber)



    context = {
        'current_page': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator,
        "Items": Items,
        'filter': documentfilter,
        'campus':campus,
        'department':department,
        'base_template':base_template,

    }

    return render(request, "docmgt/doclist.html", context)

@login_required
def fileview(request,campus,department,pagenumber):

    base_template,urlhome=param(campus,department)


    form = ViewForm(department,campus)
    # form = UploadForm()

    qs = FileInfo.objects.filter(department=department,campus=campus).order_by('-uploadtime')

    paginator,current_page,is_paginated,Items = paginate(qs,request,25,pagenumber)

    context = {
        'current_page': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator,
        "Items": Items,
        'filter': qs,
        'form': form,
        'campus':campus,
        'department':department,
        'base_template':base_template,
        'urlhome' :urlhome,
    }

    return render(request, "docmgt/upload.html", context)

@login_required
def upload(request,campus,department):
    # Handle file upload

    if request.method == 'POST':

        # form = UploadForm(request.POST, request.FILES)
        # if form.is_valid():
        files = request.FILES.getlist('file')
        catename = request.POST.get('categoryname')



        for f in files:
            path=settings.MEDIA_ROOT+"/docmgt"+"//"+campus+"//"+department
            type_excel = f.name.split('.')[-1]

            if len(f.name) > 100 :
                context = {
                    'result': 'File Name is too long',

                }
                return render(request, "docmgt/result.html", context)

            elif type_excel in ('pdf','docx','xlsx'):
                # upload files name is filename + categoryname

                randomkeyvalue = random.randint(10,9999999999)
                name = catename + str(randomkeyvalue)

                file_info = FileInfo(filename=f.name,
                                     filesize=1 if 0 < f.size < 1024 else f.size / 1024,
                                     filepath=os.path.join(path, name),


                                     category=Category.objects.get(id = catename),
                                     # department_id = Department.objects.get(password = password, department_name = department_name)
                                     uploadtime=timezone.localtime(),
                                     uploaduser=request.user.username,
                                     department=department,
                                     campus=campus
                                     )
                file_info.save()
            # 上传

                destination = open(os.path.join(path, name), 'wb+')
                for chunk in f.chunks():
                    destination.write(chunk)
                destination.close()
            else:
                context = {
                    'result': 'please choose the right format: PDF,DOCX,XLSX',

                }
                return render(request, "docmgt/result.html", context)

        # 返回上传页
        return fileview(request,campus,department,1)
        # else:
        #     print("not good")
        #     return fileview(request,campus,department,1)
    else:

        return fileview(request,campus,department,1)

@login_required
def download(request, id):
    file_info = FileInfo.objects.get(id=id)
    # print('下载的文件名：' + file_info.filename)
    file = open(file_info.filepath, 'rb')
    response = FileResponse(file)
    response['Content-Disposition'] = 'attachment;filename="%s"' % quote(file_info.filename)
    return response


@login_required
def delete(request, id, pagenumber,campus,department):

    file_info = FileInfo.objects.get(id=id)
    files = file_info.filepath
    if not files:
        return
    # fname = os.path.join(settings.MEDIA_ROOT, str(files))
    if os.path.isfile(files):
        os.remove(files)

    file_info = FileInfo.objects.get(id=id)
    file_info.delete()
    return HttpResponseRedirect(reverse('docupload', kwargs={'campus': campus,'department':department}))
    # return fileview(request,campus,department,pagenumber)

@login_required
def categoryview(request,campus,department,pagenumber):

    base_template,urlhome=param(campus,department)


    form = CategoryForm()

    qs = Category.objects.filter(department=department,campus=campus).order_by('id')

    paginator,current_page,is_paginated,Items = paginate(qs,request,25,pagenumber)

    context = {
        'current_page': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator,
        "Items": Items,
        'filter': qs,
        'form': form,
        'campus':campus,
        'department':department,
        'base_template':base_template,
        'urlhome' :urlhome,
    }

    return render(request, "docmgt/categoryadd.html", context)

@login_required
def categoryadd(request,campus,department):

    if request.method == 'POST':

        form = CategoryForm(request.POST)
        if form.is_valid():

            # permisson: group id
            selectedcheckboxlist = request.POST.get('selectedcheckbox').split(",")

            selectedcheckboxid = request.POST.get('selectedcheckbox')
            groupnamelist = []
            for groupid in selectedcheckboxlist:

                groupname = Group.objects.filter(pk = groupid).values_list('name', flat=True).distinct()[0]
                groupnamelist.append(groupname)




            new_form = form.save(commit=False)
            new_form.department = department
            new_form.campus = campus
            new_form.createtime = timezone.localtime()
            new_form.lastupdatetime = timezone.localtime()
            new_form.createuser = request.user.username
            new_form.permission = selectedcheckboxid
            new_form.permissionname = groupnamelist
            new_form.save()
            form.save_m2m()

            return categoryview(request,campus,department,1)

        else:
            return categoryview(request,campus,department,1)
    else:

        return categoryview(request,campus,department,1)


@login_required
def categoryedit(request, id, pagenumber,campus,department,categoryname,permission):

    base_template,urlhome=param(campus,department)

    instance = Category.objects.get(id=id)

    if request.method == 'POST':

        form = CategoryUpdateForm(request.POST, instance=instance)
        if form.is_valid():

            # form.save(commit=True)
            selectedcheckboxlist = request.POST.get('selectedcheckbox').split(",")

            selectedcheckboxid = request.POST.get('selectedcheckbox')
            groupnamelist = []
            for groupid in selectedcheckboxlist:

                groupname = Group.objects.filter(pk = groupid).values_list('name', flat=True).distinct()[0]
                groupnamelist.append(groupname)


            new_form = form.save(commit=False)
            new_form.lastupdatetime = timezone.localtime()
            new_form.lastupdateuser = request.user.username
            new_form.permission = selectedcheckboxid
            new_form.permissionname = groupnamelist
            new_form.save()
            form.save_m2m()

            # Category.objects.filter(id=id).update(syncuser=request.user.username,synctime=timezone.localtime())

            return HttpResponseRedirect(reverse('doccategoryadd', kwargs={'campus': campus,'department':department}))

        else:
            return HttpResponseRedirect(reverse('doccategoryadd', kwargs={'campus': campus,'department':department}))
    else:

        context = {

            'categoryname':categoryname,
            'base_template':base_template,
            'urlhome' :urlhome,
            'campus':campus,
            'department':department,
            'selectedcheckboxvalue':permission
        }

        return render(request, "docmgt/categoryedit.html", context)




@login_required
def categorydelete(request, id, pagenumber,campus,department):

    categoryitem = Category.objects.get(id=id)
    categoryitem.delete()



    return HttpResponseRedirect(reverse('doccategoryadd', kwargs={'campus': campus,'department':department}))
