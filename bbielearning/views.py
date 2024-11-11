from django.shortcuts import render
from .models import User, Course, Enrolleduser,Category,BBBRecordings,BBBbn_logs,UserBulk,BBBRecordings_Old,StudentAssignTrainer
from .model_sqlview import BBBRecordingsView,BBBRecordingsBackupView

from django_tables2 import SingleTableView
from .tables import CoursesTable, UsersTable,EnrolledusersTable,UsersPriorityTable,UserBulkTable,UsersSuspendTable
from django.views.generic import (
     ListView,
     DetailView,
     CreateView
)
import requests
import random
import xlrd
from xlrd import xldate_as_tuple
import json
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime

from django.utils import timezone
# import xmltodict
# from json_response import JsonResponse

from .filters import EnrollFilter,UserFilter,CourseFilter,UserPriorityFilter,UserSuspendFilter
from django.core.paginator import Paginator
from django.http import Http404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

@login_required
def bbihome_view(request):
    context = {
    #     'posts':Post.objects.all()
    }

    return render(request,'bbi/home.html',context)

# def permisson(request,url):
#
#     if not request.user.has_perm(url):
#         return False
#

@login_required
def paginate(f,r,itemsnumber):
    paginator = Paginator(f.qs, itemsnumber, orphans=5)

    is_paginated = True if paginator.num_pages > 1 else False
    page = r.GET.get('page') or 1
    try:
        current_page = paginator.page(page)
    except InvalidPage as e:
        raise Http404(str(e))

    try:
        Items = paginator.page(page)
    except PageNotAnInteger:
        Items = paginator.page(1)
    except EmptyPage:
        Items = paginator.page(paginator.num_pages)

    return paginator,current_page,is_paginated,Items


# @permission_required('bbielearning.view_course', raise_exception=True)
@login_required
def bbiCourse_view(request):
    #
    # if not permisson(request,"bbielearning.view_course"):
    #     return HttpResponse('403 Forbidden')

    categoryname = request.GET.get('categoryname')

    if categoryname:
        f = CourseFilter(request.GET, queryset=Course.objects.filter(categoryname=categoryname))
    else:
        f = CourseFilter(request.GET, queryset=Course.objects.all())

    table = CoursesTable(f.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    context = {'table': table, 'filter': f, }

    return render(request, "bbi/course.html", context)


    # model = Course
    # table_class = CoursesTable
    # template_name = 'course.html'

class bbiEnroll_view(SingleTableView):

    #savecourses()
    #model = Enrolleduser.objects.filter(courseid=56)
    model = Enrolleduser
    table_class = EnrolledusersTable
    template_name = 'bbi/enroll.html'

@login_required
def bbiusertest_view(request):
    f = UserFilter(request.GET, queryset=User.objects.all())

    paginator,current_page,is_paginated,Items = paginate(f,request,6)

    context = {
        'current_page': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator,
        "Items": Items,
        'filter': f,
    }

    return render(request, 'bbi/users.html', context)



@login_required
def bbiuser_view(request):
    f = UserFilter(request.GET, queryset=User.objects.all())
    # paginator = Paginator(f.qs, 30)
    # page = request.GET.get('page')
    # page_obj = paginator.get_page(page)
    #
    # return render(request, 'users.html', context)

    table = UsersTable(f.qs,studentidname='Studentid')
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    context = {'table': table, 'filter': f,}

    return render(request, "bbi/user.html", context)

@login_required
def bbiuserpriority_view(request):

    if request.GET.get('prioritybtn'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        User.objects.filter(pk__in=selectedcheckboxid).update(priority="Priority")

        userids = User.objects.filter(pk__in=selectedcheckboxid).values('userid')

        for id in userids:
        #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = id["userid"]

            request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
            url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+userid+'&users[0][icq]=Priority'
            res = requests.post(url)

    if request.GET.get('nullvalue'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        User.objects.filter(pk__in=selectedcheckboxid).update(priority="")

        userids = User.objects.filter(pk__in=selectedcheckboxid).values('userid')

        for id in userids:
        #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = id["userid"]

            request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
            url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+userid+'&users[0][icq]='
            res = requests.post(url)


    f = UserPriorityFilter(request.GET, queryset=User.objects.all())

    table = UsersPriorityTable(f.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    context = {'table': table, 'filter': f, }

    return render(request, "bbi/userpriority.html", context)


@login_required
# suspend user in user mangement
def bbiusersuspend_view(request):

    if request.GET.get('suspendbtn'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        User.objects.filter(pk__in=selectedcheckboxid).update(suspended=True)

        userids = User.objects.filter(pk__in=selectedcheckboxid).values('userid')

        for id in userids:
        #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = id["userid"]

            request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
            url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+userid+'&users[0][suspended]=1'
            res = requests.post(url)

    if request.GET.get('activebtn'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        User.objects.filter(pk__in=selectedcheckboxid).update(suspended=False)

        userids = User.objects.filter(pk__in=selectedcheckboxid).values('userid')

        for id in userids:
        #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = id["userid"]

            request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
            url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+userid+'&users[0][suspended]=0'
            res = requests.post(url)


    f = UserSuspendFilter(request.GET, queryset=User.objects.all())

    table = UsersSuspendTable(f.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    context = {'table': table, 'filter': f, }

    return render(request, "bbi/usersuspend.html", context)

@login_required
def bbiuserbulkcreate_view(request):

    randomkeyvalue = 1
    msg=''

    if request.method == "POST":
        if request.POST.get('upload'):
            randomkeyvalue = random.randint(0,9999999999)
            f = request.FILES['my_file']
            type_excel = f.name.split('.')[-1]

            if 'xlsx' == type_excel:
                # 开始解析上传的excel表格
                wb = xlrd.open_workbook(filename=None, file_contents=f.read())  # 关键点在于这里
                table = wb.sheets()[0]
                nrows = table.nrows  # 行数
                # ncole = table.ncols  # 列数

                for i in range(1, nrows):
                    # if 4 == i:
                    #     i/0
                    rowValues = table.row_values(i)  # 一行的数据
                    UserBulkitem = UserBulk()

                    UserBulkitem.username = rowValues[0]
                    UserBulkitem.firstname = rowValues[1]
                    UserBulkitem.lastname = rowValues[2]
                    # date = datetime(*xldate_as_tuple(rowValues[3], wb.datemode))
                    # # password = str(date)[8:10]+str(date)[5:7]+str(date)[0:4]
                    # print(rowValues[0],rowValues[1],rowValues[3],date)
                    # date=str(date).split( )[0]
                    # print (date)
                    # password = date.split('-')[2]+date.split('-')[1]+date.split('-')[0]
                    date = str(rowValues[3])
                    password = date.split('/')[0]+date.split('/')[1]+date.split('/')[2]
                    print(password)
                    UserBulkitem.password = password

                    UserBulkitem.email = rowValues[4]
                    UserBulkitem.createduser = request.user.username
                    UserBulkitem.createdtime = timezone.localtime()
                    UserBulkitem.randomkey = randomkeyvalue

                    UserBulkitem.save()

                qs = UserBulk.objects.all().filter(randomkey = randomkeyvalue)


                table = UserBulkTable(qs)

                sync = 1

                context = {'table': table, 'filter': qs, 'sync':sync,'randomkey':randomkeyvalue}

                return render(request, "bbi/userbulkcreate.html", context)
            # try:
            #     with transaction.atomic():
            #
            # #             good = models.GoodsManage.objects.get(international_code=rowValues[0])
            # #             models.SupplierGoodsManage.objects.create(goods=good, sale_price=rowValues[1],sale_min_count = rowValues[2])
            # except Exception as e:
            #     msg= "Something Wrong...."
            else:
                msg= "this is not xlsx"
                context = {'result': msg, }
                return render(request, "bbi/result.html", context)

        if request.POST.get('sync'):
            randomkeyvalue = request.POST.get('randomkey')

            usersqs = UserBulk.objects.filter(randomkey=randomkeyvalue).values('username','firstname','lastname','password','email')

            for useritem in usersqs:
            #print(id["courseid"])values_list('courseid', flat=True).distinct()
                username = useritem["username"]
                firstname = useritem["firstname"]

                lastname = useritem["lastname"]
                password = useritem["password"]
                email = useritem["email"]
                city = "Sydney"
                country = "Australia"


                request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
                url1 = request_url+'&wsfunction=core_user_create_users&'+'&users[0][username]='+username+'&users[0][firstname]='+firstname
                url2 = url1 + '&users[0][lastname]='+lastname+'&users[0][password]='+password+'&users[0][email]='+email
                url = url2 + '&users[0][city]='+city+'&users[0][country]='+country
                res = requests.post(url)

            UserBulk.objects.filter(randomkey=randomkeyvalue).update(syncuser=request.user.username,synctime=timezone.localtime())
            context = {'result': "Sync is finished", }
            return render(request, "bbi/result.html", context)


    else:
        # qs should be null
        qs = UserBulk.objects.all().filter(randomkey = "")


        table = UserBulkTable(qs)


        context = {'table': table, 'filter': qs,}

        return render(request, "bbi/userbulkcreate.html", context)


@login_required
def bbisync(request):

    return render(request, 'bbi/sync.html' )

@login_required
def bbienrolluser_view(request):

    categoryid = request.GET.get('categoryselect')
    courseid = request.GET.get('course_id')
    studentid = request.GET.get('user')
    selectIndexid = request.GET.get('selectIndex')

    if request.GET.get('suspend'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")
        #print(selectedcheckboxid)
        enrolleduser = Enrolleduser()
        # enrolleduser.id = selectedcheckboxid
        # enrolleduser.suspended = True
        # enrolleduser.save()
        Enrolleduser.objects.filter(pk__in= selectedcheckboxid).update(suspended="suspended")

        for itemid in selectedcheckboxid:
            #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = Enrolleduser.objects.filter(pk = itemid).values_list('userid', flat=True).distinct()[0]
            roleid = Enrolleduser.objects.filter(pk = itemid).values_list('roleid', flat=True).distinct()[0].split(",")[0]

            request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
            url = request_url+'&wsfunction=enrol_manual_enrol_users'+'&enrolments[0][courseid]='+courseid+'&enrolments[0][roleid]='+roleid+'&enrolments[0][userid]='+userid+'&enrolments[0][suspend]=1'
            res = requests.post(url)


    elif request.GET.get('unsuspend'):

        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        enrolleduser = Enrolleduser()

        Enrolleduser.objects.filter(pk__in=selectedcheckboxid).update(suspended="active")

        for itemid in selectedcheckboxid:
            #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = Enrolleduser.objects.filter(pk = itemid).values_list('userid', flat=True).distinct()[0]
            roleid = Enrolleduser.objects.filter(pk = itemid).values_list('roleid', flat=True).distinct()[0].split(",")[0]

            request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
            url = request_url+'&wsfunction=enrol_manual_enrol_users'+'&enrolments[0][courseid]='+courseid+'&enrolments[0][roleid]='+roleid+'&enrolments[0][userid]='+userid+'&enrolments[0][suspend]=0'
            res = requests.post(url)

    # categoryid = request.GET.get('categoryselect')
    # courseid = request.GET.get('course_id')
    # studentid = request.GET.get('user')
    # selectIndexid = request.GET.get('selectIndex')

    if studentid:
        username = studentid.split(",")
        f = Enrolleduser.objects.all().filter(courseid = courseid, username__in = username).order_by('username')

    else:

        f = Enrolleduser.objects.all().filter(courseid = courseid).order_by('username')
    paginator = Paginator(f, 30)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    courseobj=Course.objects.all()
    categoryobj=Category.objects.all()
    context = {'page_obj': page_obj,
               'paginator': paginator,
               'is_paginated': True,
               'coursedata':courseobj,
               'categorydata':categoryobj ,
               'filter': f,
               }
    return render(request, 'bbi/enrolluser.html', context)

@login_required
# suspend users in course
def bbibulksuspendusers_view(request):

    categoryid = request.GET.get('categoryselect')
    courseid = request.GET.get('course_id')
    #studentid = request.GET.get('user')
    #selectIndexid = request.GET.get('selectIndex')

    if request.GET.get('sync'):
        Enrolleduser.objects.all().filter(courseid = courseid).delete()
        #for id in [{'courseid': '107'}]:

        request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
        url = request_url+'&wsfunction=core_enrol_get_enrolled_users&moodlewsrestformat=json'+'&courseid='+courseid
        #url = request_url+'&wsfunction=core_enrol_get_enrolled_users&moodlewsrestformat=json'+'&courseid=3'
        res = requests.post(url)
        enrolleduser_result = json.loads(res.text)

        for enrolleduser in enrolleduser_result:
            roleid = []
            rolename = []
            issuspended = "suspended"

            # result = Enrolleduser.objects.all().filter(courseid = courseid, userid = enrolleduser["id"])


            for roleitem in enrolleduser["roles"]:
                roleid.append(str(roleitem["roleid"]))
                rolename.append(roleitem["shortname"])

            if "enrolledcourses" in enrolleduser:

                for enroll in enrolleduser["enrolledcourses"]:
                    # print ("enrollid",type(enroll["id"]))
                    # print ("courseid",type(id["courseid"]))
                    if enroll["id"] is not None:
                        if courseid == str(enroll["id"]):

                            issuspended = "active"


            enrollitem = Enrolleduser()
            enrollitem.courseid = courseid
            enrollitem.userid = enrolleduser["id"]
            enrollitem.username = enrolleduser["username"]
            enrollitem.fullname = enrolleduser["fullname"]
            enrollitem.suspended = issuspended
            enrollitem.roleid = ','.join(roleid)
            enrollitem.rolename =','.join(rolename)

            enrollitem.save()


    if request.GET.get('suspend'):
    #selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")
    #print(selectedcheckboxid)
        enrolleduser = Enrolleduser()
        # enrolleduser.id = selectedcheckboxid
        # enrolleduser.suspended = True
        # enrolleduser.save()
        Enrolleduser.objects.filter(courseid = courseid, roleid = 5).update(suspended="suspended")
        userids = Enrolleduser.objects.filter(courseid = courseid, roleid = 5).values('userid')

        for id in userids:
        #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = id["userid"]
            roleid = 5
            request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
            url = request_url+'&wsfunction=enrol_manual_enrol_users'+'&enrolments[0][courseid]='+courseid+'&enrolments[0][roleid]=5'+'&enrolments[0][userid]='+userid+'&enrolments[0][suspend]=1'
            res = requests.post(url)



    f = Enrolleduser.objects.all().filter(courseid = courseid).order_by('username')
    paginator = Paginator(f, 30)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    courseobj=Course.objects.all()
    categoryobj=Category.objects.all()
    context = {'page_obj': page_obj,
               'paginator': paginator,
               'is_paginated': True,
               'coursedata':courseobj,
               'categorydata':categoryobj ,
               'filter': f,
               }
    return render(request, 'bbi/bulksuspendusers.html', context)

@login_required
def bbistudentassigntrainer(request):

    categoryid = request.GET.get('categoryselect')
    courseid = request.GET.get('course_id')
    pageupdate = 1
    #studentid = request.GET.get('user')
    #selectIndexid = request.GET.get('selectIndex')

    if request.GET.get('sync'):
        # Enrolleduser.objects.all().filter(courseid = courseid).delete()
        #for id in [{'courseid': '107'}]:

        request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
        url = request_url+'&wsfunction=core_enrol_get_enrolled_users&moodlewsrestformat=json'+'&courseid='+courseid
        #url = request_url+'&wsfunction=core_enrol_get_enrolled_users&moodlewsrestformat=json'+'&courseid=3'
        res = requests.post(url)
        enrolleduser_result = json.loads(res.text)

        for enrolleduser in enrolleduser_result:
            roleid = []
            rolename = []
            issuspended = "suspended"

            result = StudentAssignTrainer.objects.all().filter(courseid = courseid, userid = enrolleduser["id"])


            for roleitem in enrolleduser["roles"]:
                roleid.append(str(roleitem["roleid"]))
                rolename.append(roleitem["shortname"])

            if "enrolledcourses" in enrolleduser:

                for enroll in enrolleduser["enrolledcourses"]:
                    # print ("enrollid",type(enroll["id"]))
                    # print ("courseid",type(id["courseid"]))
                    if enroll["id"] is not None:
                        if courseid == str(enroll["id"]):

                            issuspended = "active"


            enrollitem = StudentAssignTrainer()
            enrollitem.courseid = courseid
            enrollitem.userid = enrolleduser["id"]
            enrollitem.username = enrolleduser["username"]
            enrollitem.fullname = enrolleduser["fullname"]
            enrollitem.suspended = issuspended
            enrollitem.roleid = ','.join(roleid)
            enrollitem.rolename =','.join(rolename)

            if not result:
                enrollitem.save()
            else:
                StudentAssignTrainer.objects.filter(courseid = courseid, userid = enrolleduser["id"]).update(suspended=issuspended)


    if request.GET.get('assign'):
        trainer = request.GET.get('trainerselect')
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        StudentAssignTrainer.objects.filter(pk__in=selectedcheckboxid).update(trainername=trainer)
        if request.GET.get('page'):
            pageupdate = request.GET.get('page')

    if request.GET.get('none'):
        # trainer = request.GET.get('trainerselect')
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        StudentAssignTrainer.objects.filter(pk__in=selectedcheckboxid).update(trainername="")
        if request.GET.get('page'):
            pageupdate = request.GET.get('page')


    if request.GET.get('deletesingle'):
    # trainer = request.GET.get('trainerselect')
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        StudentAssignTrainer.objects.filter(pk__in=selectedcheckboxid).delete()
        if request.GET.get('page'):
            pageupdate = request.GET.get('page')



    if request.GET.get('delete'):
        courseid = request.GET.get('course_id')

        StudentAssignTrainer.objects.filter(courseid=courseid).delete()


    f = StudentAssignTrainer.objects.all().filter(courseid = courseid,roleid = 5,suspended="active").order_by('username')
    paginator = Paginator(f, 30)
    if int(pageupdate) > 1:
        page=pageupdate
    else:
        page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    courseobj=Course.objects.all()
    categoryobj=Category.objects.all()
    trainerobj = StudentAssignTrainer.objects.all().filter(courseid = courseid,roleid = 3)
    context = {'page_obj': page_obj,
               'paginator': paginator,
               'is_paginated': True,
               'coursedata':courseobj,
               'categorydata':categoryobj ,
               'trainerdata':trainerobj ,
               'filter': f,
               }
    return render(request, 'bbi/studentassigntrainer.html', context)

@login_required
def bbiSaveuser_View(request):
    request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
    url = request_url+'&wsfunction=core_user_get_users&moodlewsrestformat=json&criteria[0][key]=email&criteria[0][value]=%'
    res = requests.get(url)
    users_result = json.loads(res.text)

    User.objects.all().delete()

    for useritem in users_result["users"]:
        Users = User()
        Users.userid = useritem["id"]
        Users.username = useritem["username"]
        Users.firstname = useritem["firstname"]
        Users.lastname = useritem["lastname"]
        Users.fullname = useritem["fullname"]
        Users.email = useritem["email"]
        Users.suspended = useritem["suspended"]
        if "icq" in useritem:
            Users.priority = useritem["icq"]

        Users.save()
    context = {
          "completed": "Completed to sync all the users",
    }
    return render(request,'bbi/sync.html',context)

def bbiUpdateusersuspended_View(request):
    userid = User.objects.all().filter(suspended=True).values('userid')

    for id in userid:
        #print(id["courseid"])
        request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
        url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+id["userid"]+'users[0][suspended]=0'
        #res = requests.post(url)
        # grades_result = json.loads(res.text)
        # print(grades_result)

    context = {
          "completed": 1
    }
    return render(request,'bbi/sync.html',context)

@login_required
def bbiSavecourses_View(request):

    request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
    url = request_url+'&wsfunction=core_course_get_categories&moodlewsrestformat=json'
    res = requests.get(url)
    categories_result = json.loads(res.text)

    Category.objects.all().delete()

    for categoryitem in categories_result:
        category = Category()
        if categoryitem["parent"] > 0 and categoryitem["visible"] == 1:
            category.categoryid = categoryitem["id"]
            category.categoryname = categoryitem["name"]


            category.save()


    request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
    url = request_url+'&wsfunction=core_course_get_courses&moodlewsrestformat=json'
    res = requests.get(url)
    courses_result = json.loads(res.text)

    Course.objects.all().delete()

    for course in courses_result:
        courses = Course()
        courses.courseid = course["id"]
        courses.coursename = course["fullname"]
        courses.categoryid = course["categoryid"]

        categoryid=course["categoryid"]
        # print(categoryid)
        # print(course["fullname"])
        IScategoryname=Category.objects.filter(categoryid = categoryid).values_list('categoryname', flat=True).distinct()
        if IScategoryname:
            categoryname=IScategoryname[0]
            #print(categoryname)
            courses.categoryname =  categoryname
            courses.save()




    context = {
          "completed": "Completed to sync the categorys and courses",
    }

    return render(request,'bbi/sync.html',context)

@login_required
def bbiSaveenrolleduser_View(request):
    coursesid = Course.objects.all().values('courseid')

    Enrolleduser.objects.all().delete()
    #for id in [{'courseid': '107'}]:
    for id in coursesid:
        courseiditem = id["courseid"]
        request_url = 'https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php?wstoken=f47fac7e6cd22e388d9a90e3b86c4a1f'
        url = request_url+'&wsfunction=core_enrol_get_enrolled_users&moodlewsrestformat=json'+'&courseid='+id["courseid"]
        #url = request_url+'&wsfunction=core_enrol_get_enrolled_users&moodlewsrestformat=json'+'&courseid=3'
        res = requests.post(url)
        enrolleduser_result = json.loads(res.text)

        for enrolleduser in enrolleduser_result:
            roleid = []
            rolename = []
            issuspended = "suspended"


            for roleitem in enrolleduser["roles"]:
                roleid.append(str(roleitem["roleid"]))
                rolename.append(roleitem["shortname"])

            if "enrolledcourses" in enrolleduser:

                for enroll in enrolleduser["enrolledcourses"]:
                    # print ("enrollid",type(enroll["id"]))
                    # print ("courseid",type(id["courseid"]))
                    if enroll["id"] is not None:
                        if courseiditem == str(enroll["id"]):

                            issuspended = "active"


            enrollitem = Enrolleduser()
            enrollitem.courseid = id["courseid"]
            enrollitem.userid = enrolleduser["id"]
            enrollitem.username = enrolleduser["username"]
            enrollitem.fullname = enrolleduser["fullname"]
            enrollitem.suspended = issuspended
            enrollitem.roleid = ','.join(roleid)
            enrollitem.rolename =','.join(rolename)
            enrollitem.save()

    context = {
          "completed": "Completed to sync all Enrolledusers"
    }
    return render(request,'bbi/sync.html',context)

@login_required
def bbiBBBrecord_View(request):
    categoryid = request.GET.get('categoryselect')
    courseid = request.GET.get('course_id')
    selectIndexid = request.GET.get('selectIndex')


    f = BBBRecordingsBackupView.objects.all().filter(courseid = courseid).order_by('starttime')

    paginator = Paginator(f, 30)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    courseobj=Course.objects.all()
    categoryobj=Category.objects.all()
    context = {'page_obj': page_obj,
               'paginator': paginator,
               'is_paginated': True,
               'coursedata':courseobj,
               'categorydata':categoryobj ,
               'filter': f,
               }
    return render(request, 'bbi/BBBview.html', context)


@login_required
def bbiBBBrecordDelete_View(request):

    categoryid = request.GET.get('categoryselect')
    courseid = request.GET.get('course_id')
    selectIndexid = request.GET.get('selectIndex')

    if request.GET.get('delete'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        recordids = BBBRecordings.objects.all().filter(pk__in= selectedcheckboxid).values('recordid')

        for record in recordids:

            request_url = 'https://b01.cgcloud.com.au/bigbluebutton/api/deleteRecordings?'
            request_params = 'deleteRecordingsrecordID='+record["recordid"]+'OvTuHB1E0DB96bDfJiHJ2OAE9lsarU6JGQznB6iQ0c4'

            checksum = hashlib.sha1(request_params.encode('utf-8')).hexdigest()

            url = request_url + 'recordID='+record["recordid"]+'&checksum='+checksum

            res = requests.post(url)

        BBBRecordings.objects.filter(pk__in= selectedcheckboxid).delete()

    if courseid:
        f = BBBRecordingsView.objects.all().filter(courseid = courseid).order_by('starttime')
    else:
        f = BBBRecordingsView.objects.all().order_by('starttime')

    paginator = Paginator(f, 30)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    courseobj=Course.objects.all()
    categoryobj=Category.objects.all()
    context = {'page_obj': page_obj,
               'paginator': paginator,
               'is_paginated': True,
               'coursedata':courseobj,
               'categorydata':categoryobj ,
               'filter': f,
               }
    return render(request, 'bbi/BBBdelete.html', context)

@login_required
def bbiSaveBBBrecord_View(request):
    metas = BBBbn_logs.objects.all().filter(log="Callback").values('meta')

    BBBRecordings.objects.all().delete()


    request_url = 'https://b01.cgcloud.com.au/bigbluebutton/api/getRecordings?'
    # request_url = 'http://10.0.0.7/bigbluebutton/api/getRecordings?'
    request_params = 'getRecordingsOvTuHB1E0DB96bDfJiHJ2OAE9lsarU6JGQznB6iQ0c4'

    # checksum = hashlib.sha1(request_params.encode('utf-8')).hexdigest()
    checksum = hashlib.sha1(request_params.encode('utf-8')).hexdigest()
    url = request_url + '&checksum='+checksum
    # url = request_url + '&checksum=80912947ef716a62fdbbf4cfc01454ceb2e7c6e4'

    res = requests.post(url).text
    # print(res.text)
    # recording_result = json.loads(res.text)
    # xmlparse = xmltodict.parse(res)
    root = ET.fromstring(res)
    # print(root[1])
    # for level1 in root:
    #     print(level1)
    #     if level1 == "recordings":
    #         print("recordings is true")
    for record in root[1]:
            records = BBBRecordings()
            records.recordid = record[0].text
            records.meetingid = record[1].text
            records.name = record[3].text
            records.published = record[5].text
            records.state = record[6].text
            records.starttime = record[7].text
            records.endtime= record[8].text
            records.save()

    # jsonstr = json.load(xmlparse)
    # print(jsonstr)
    # for recording in jsonstr[recordings]:
    #
    #
        #

    context = {
          "completed": "Completed to sync all Recordings"
    }
    return render(request,'bbi/sync.html',context)

@login_required
def bbiSaveBBBrecord_Backup(request):
    metas = BBBbn_logs.objects.all().filter(log="Callback").values('meta')

    BBBRecordings_Old.objects.all().delete()

    request_url = 'http://10.0.0.7/bigbluebutton/api/getRecordings?'
    # request_url = 'http://10.0.0.7/bigbluebutton/api/getRecordings?'
    request_params = 'getRecordingsigFRYGZHNkrQ5DkEm7Z2VAwfVVz77CbcjjT76L2U'

    # checksum = hashlib.sha1(request_params.encode('utf-8')).hexdigest()
    url = request_url + '&checksum=80912947ef716a62fdbbf4cfc01454ceb2e7c6e4'
    # url = request_url + '&checksum=80912947ef716a62fdbbf4cfc01454ceb2e7c6e4'

    res = requests.post(url).text
    # print(res.text)
    # recording_result = json.loads(res.text)
    # xmlparse = xmltodict.parse(res)
    root = ET.fromstring(res)
    # print(root[1])
    # for level1 in root:
    #     print(level1)
    #     if level1 == "recordings":
    #         print("recordings is true")
    for record in root[1]:
            records = BBBRecordings_Old()
            records.recordid = record[0].text
            records.meetingid = record[1].text
            records.name = record[3].text
            records.published = record[5].text
            records.state = record[6].text
            records.starttime = record[7].text
            records.endtime= record[8].text
            records.save()

    # jsonstr = json.load(xmlparse)
    # print(jsonstr)
    # for recording in jsonstr[recordings]:
    #
    #
        #

    context = {
          "completed": "Completed to sync all Recordings"
    }
    return render(request,'bbi/sync.html',context)
