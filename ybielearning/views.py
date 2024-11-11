from django.shortcuts import render
from .models import User, Course, Enrolleduser,Category,BBBRecordings,BBBbn_logs,UserBulk
from .model_sqlview import BBBRecordingsView,BBBRecordingsBackupView

from django_tables2 import SingleTableView
from .tables import CoursesTable, UsersTable,EnrolledusersTable,UserBulkTable,UsersPriorityTable,UsersSuspendTable
from django.views.generic import (
     ListView,
     DetailView,
     CreateView
)
import requests
import json
import hashlib
import random
import xlrd
from xlrd import xldate_as_tuple
#from json_response import JsonResponse
import xml.etree.ElementTree as ET
from .filters import EnrollFilter,UserFilter,CourseFilter,UserPriorityFilter,UserSuspendFilter
from django.core.paginator import Paginator
from datetime import datetime

from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def Ybihome_view(request):
    context = {
    #     'posts':Post.objects.all()
    }

    return render(request,'home.html',context)

@login_required
def Course_view(request):

    categoryname = request.GET.get('categoryname')

    if categoryname:
        f = CourseFilter(request.GET, queryset=Course.objects.filter(categoryname=categoryname))
    else:
        f = CourseFilter(request.GET, queryset=Course.objects.all())

    table = CoursesTable(f.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    context = {'table': table, 'filter': f, }

    return render(request, "course.html", context)


    # model = Course
    # table_class = CoursesTable
    # template_name = 'course.html'

class Enroll_view(SingleTableView):

    #savecourses()
    #model = Enrolleduser.objects.filter(courseid=56)
    model = Enrolleduser
    table_class = EnrolledusersTable
    template_name = 'enroll.html'

@login_required
def user_view(request):
    f = UserFilter(request.GET, queryset=User.objects.all())
    # paginator = Paginator(f.qs, 30)
    # page = request.GET.get('page')
    # page_obj = paginator.get_page(page)
    #
    # return render(request, 'users.html', context)

    table = UsersTable(f.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    context = {'table': table, 'filter': f, }

    return render(request, "user.html", context)

@login_required
def ybiuserbulkcreate_view(request):

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

                return render(request, "userbulkcreate.html", context)
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
                return render(request, "result.html", context)

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


                request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
                url1 = request_url+'&wsfunction=core_user_create_users&'+'&users[0][username]='+username+'&users[0][firstname]='+firstname
                url2 = url1 + '&users[0][lastname]='+lastname+'&users[0][password]='+password+'&users[0][email]='+email
                url = url2 + '&users[0][city]='+city+'&users[0][country]='+country
                res = requests.post(url)

            UserBulk.objects.filter(randomkey=randomkeyvalue).update(syncuser=request.user.username,synctime=timezone.localtime())
            context = {'result': "Sync is finished", }
            return render(request, "result.html", context)


    else:
        # qs should be null
        qs = UserBulk.objects.all().filter(randomkey = "")


        table = UserBulkTable(qs)


        context = {'table': table, 'filter': qs,}

        return render(request, "userbulkcreate.html", context)

@login_required
def ybiuserpriority_view(request):

    if request.GET.get('prioritybtn'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        User.objects.filter(pk__in=selectedcheckboxid).update(priority="Priority")

        userids = User.objects.filter(pk__in=selectedcheckboxid).values('userid')

        for id in userids:
        #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = id["userid"]

            request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
            url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+userid+'&users[0][icq]=Priority'
            res = requests.post(url)

    if request.GET.get('nullvalue'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        User.objects.filter(pk__in=selectedcheckboxid).update(priority="")

        userids = User.objects.filter(pk__in=selectedcheckboxid).values('userid')

        for id in userids:
        #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = id["userid"]

            request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
            url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+userid+'&users[0][icq]='
            res = requests.post(url)


    f = UserPriorityFilter(request.GET, queryset=User.objects.all())

    table = UsersPriorityTable(f.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    context = {'table': table, 'filter': f, }

    return render(request, "userpriority.html", context)

@login_required
# suspend user in user mangement
def ybiusersuspend_view(request):

    if request.GET.get('suspendbtn'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        User.objects.filter(pk__in=selectedcheckboxid).update(suspended=True)

        userids = User.objects.filter(pk__in=selectedcheckboxid).values('userid')

        for id in userids:
        #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = id["userid"]

            request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
            url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+userid+'&users[0][suspended]=1'
            res = requests.post(url)

    if request.GET.get('activebtn'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        User.objects.filter(pk__in=selectedcheckboxid).update(suspended=False)

        userids = User.objects.filter(pk__in=selectedcheckboxid).values('userid')

        for id in userids:
        #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = id["userid"]

            request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
            url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+userid+'&users[0][suspended]=0'
            res = requests.post(url)


    f = UserSuspendFilter(request.GET, queryset=User.objects.all())

    table = UsersSuspendTable(f.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    context = {'table': table, 'filter': f, }

    return render(request, "usersuspend.html", context)

@login_required
def sync(request):

    return render(request, 'sync.html' )

@login_required
def enrolluser_view(request):

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
            roleid = Enrolleduser.objects.filter(pk = itemid).values_list('roleid', flat=True).distinct()[0]

            request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
            url = request_url+'&wsfunction=enrol_manual_enrol_users'+'&enrolments[0][courseid]='+courseid+'&enrolments[0][roleid]='+roleid+'&enrolments[0][userid]='+userid+'&enrolments[0][suspend]=1'
            res = requests.post(url)


    elif request.GET.get('unsuspend'):

        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        enrolleduser = Enrolleduser()

        Enrolleduser.objects.filter(pk__in=selectedcheckboxid).update(suspended="active")

        for itemid in selectedcheckboxid:
            #print(id["courseid"])values_list('courseid', flat=True).distinct()
            userid = Enrolleduser.objects.filter(pk = itemid).values_list('userid', flat=True).distinct()[0]
            roleid = Enrolleduser.objects.filter(pk = itemid).values_list('roleid', flat=True).distinct()[0]

            request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
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
    return render(request, 'enrolluser.html', context)

@login_required
def bulksuspendusers_view(request):

    categoryid = request.GET.get('categoryselect')
    courseid = request.GET.get('course_id')
    #studentid = request.GET.get('user')
    #selectIndexid = request.GET.get('selectIndex')

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
            request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
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
    return render(request, 'bulksuspendusers.html', context)

@login_required
def YbiSaveuser_View(request):
    request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
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
    return render(request,'sync.html',context)

def YbiUpdateusersuspended_View(request):
    userid = User.objects.all().filter(suspended=True).values('userid')

    for id in userid:
        #print(id["courseid"])
        request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
        url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+id["userid"]+'users[0][suspended]=0'
        #res = requests.post(url)
        # grades_result = json.loads(res.text)
        # print(grades_result)

    context = {
          "completed": 1
    }
    return render(request,'sync.html',context)

@login_required
def YbiSavecourses_View(request):

    request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
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


    request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
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

    return render(request,'sync.html',context)

@login_required
def YbiSaveenrolleduser_View(request):
    coursesid = Course.objects.all().values('courseid')
    Enrolleduser.objects.all().delete()
    for id in coursesid:
        courseiditem = id["courseid"]
        request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=ca63fdd9b6015b182726180e247d7177'
        url = request_url+'&wsfunction=core_enrol_get_enrolled_users&moodlewsrestformat=json'+'&courseid='+id["courseid"]
        #url = request_url+'&wsfunction=core_enrol_get_enrolled_users&moodlewsrestformat=json'+'&courseid=3'
        res = requests.post(url)
        enrolleduser_result = json.loads(res.text)

        for enrolleduser in enrolleduser_result:
            roleid = 1
            rolename = ""
            issuspended = "suspended"


            for roleitem in enrolleduser["roles"]:
                roleid = roleitem["roleid"]
                rolename = roleitem["shortname"]

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
            enrollitem.roleid = roleid
            enrollitem.rolename = rolename
            enrollitem.save()

    context = {
          "completed": "Completed to sync all Enrolledusers"
    }
    return render(request,'sync.html',context)


@login_required
def YbiBBBrecord_View(request):
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
    return render(request, 'BBBview.html', context)

@login_required
def YbiBBBrecordDelete_View(request):

    categoryid = request.GET.get('categoryselect')
    courseid = request.GET.get('course_id')
    selectIndexid = request.GET.get('selectIndex')

    if request.GET.get('delete'):
        selectedcheckboxid = request.GET.get('selectedcheckbox').split(",")

        recordids = BBBRecordings.objects.all().filter(pk__in= selectedcheckboxid).values('recordid')

        for record in recordids:

            request_url = 'https://b01.cgcloud.com.au/bigbluebutton/api/deleteRecordings?'
            request_params = 'deleteRecordingsrecordID='+record["recordid"]+'igFRYGZHNkrQ5DkEm7Z2VAwfVVz77CbcjjT76L2U'

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
    return render(request, 'BBBdelete.html', context)

@login_required
def YbiSaveBBBrecord_View(request):
    metas = BBBbn_logs.objects.all().filter(log="Callback").values('meta')

    BBBRecordings.objects.all().delete()

    request_url = 'https://b01.cgcloud.com.au/bigbluebutton/api/getRecordings?'
    # request_url = 'http://10.0.0.7/bigbluebutton/api/getRecordings?'
    request_params = 'getRecordingsigFRYGZHNkrQ5DkEm7Z2VAwfVVz77CbcjjT76L2U'

    # checksum = hashlib.sha1(request_params.encode('utf-8')).hexdigest()
    url = request_url + '&checksum=91218e7f70b3824ece5b20c8f2bd4777cba95f86'
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
    return render(request,'sync.html',context)
