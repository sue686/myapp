from django.shortcuts import render
from .models import User, Course, Enrolleduser,Category

from django_tables2 import SingleTableView
from .tables import CoursesTable, UsersTable,EnrolledusersTable
from django.views.generic import (
     ListView,
     DetailView,
     CreateView
)
import requests
import json
#from json_response import JsonResponse

from .filters import EnrollFilter,UserFilter,CourseFilter
from django.core.paginator import Paginator



def Ybihome_view(request):
    context = {
    #     'posts':Post.objects.all()
    }

    return render(request,'home.html',context)

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

def sync(request):

    return render(request, 'sync.html' )

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

            request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=c58d03264633223fc0b6b31b7f7f4eae'
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

            request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=c58d03264633223fc0b6b31b7f7f4eae'
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
            request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=c58d03264633223fc0b6b31b7f7f4eae'
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

def YbiSaveuser_View(request):
    request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=c58d03264633223fc0b6b31b7f7f4eae'
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

        Users.save()
    context = {
          "completed": "Completed to sync all the users",
    }
    return render(request,'sync.html',context)

def YbiUpdateusersuspended_View(request):
    userid = User.objects.all().filter(suspended=True).values('userid')

    for id in userid:
        #print(id["courseid"])
        request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=c58d03264633223fc0b6b31b7f7f4eae'
        url = request_url+'&wsfunction=core_user_update_users&'+'&users[0][id]='+id["userid"]+'users[0][suspended]=0'
        #res = requests.post(url)
        # grades_result = json.loads(res.text)
        # print(grades_result)

    context = {
          "completed": 1
    }
    return render(request,'sync.html',context)


def YbiSavecourses_View(request):

    request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=c58d03264633223fc0b6b31b7f7f4eae'
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


    request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=c58d03264633223fc0b6b31b7f7f4eae'
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

def YbiSaveenrolleduser_View(request):
    coursesid = Course.objects.all().values('courseid')
    Enrolleduser.objects.all().delete()
    for id in coursesid:
        courseiditem = id["courseid"]
        request_url = 'https://elearning.york.edu.au/webservice/rest/server.php?wstoken=c58d03264633223fc0b6b31b7f7f4eae'
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
