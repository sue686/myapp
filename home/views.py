from django.shortcuts import render
from django.core.paginator import Paginator
from docmgt.models import FileInfo
from blog.models import Post
from academic.models import AcademicCalendar
from .filters import FileFilter,PostFilter,AcademicCalendarFilter
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
import math
import requests
from django.contrib.auth.decorators import login_required

# for all the apps to get paginate function
def paginate(qs,r,itemsnumber,currentpage):
    paginator = Paginator(qs, itemsnumber)

    is_paginated = True if paginator.num_pages > 1 else False
    if r.GET.get('page'):
        page = r.GET.get('page')
    else:
        page = currentpage
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

@login_required
def home_redirect(request):

    campus = "weg"

    nowtime = timezone.localtime()
    nowyear = nowtime.year


    return HttpResponseRedirect(reverse('home', kwargs={'campus': campus,'year':nowyear}))

@login_required
def releasenotes(request):


    return render(request,'home/releasenotes.html')

@login_required
def home_view(request,campus,year):

    nowtime = timezone.localtime()
    nowyear = nowtime.year

    # Document View
    # documentfilter = FileFilter(request.GET, queryset=FileInfo.objects.filter(campus=campus).order_by('-uploadtime'))



    # Notice View
    noticefilter = PostFilter(request.GET, queryset=Post.objects.all().order_by('-top','-updatedate'))
    paginator,current_page,is_paginated,Items = paginate(noticefilter.qs,request,10,1)

    # Academic Calendar view
    calendardates2020filter = AcademicCalendarFilter(request.GET, queryset=AcademicCalendar.objects.filter(year=2020).order_by('id'))
    calendardates2021filter = AcademicCalendarFilter(request.GET, queryset=AcademicCalendar.objects.filter(year=2021).order_by('id'))
    calendardates2022filter = AcademicCalendarFilter(request.GET, queryset=AcademicCalendar.objects.filter(year=2022).order_by('id'))
    calendardates = {
            'calendardates2020filter':calendardates2020filter.qs,
            'calendardates2021filter':calendardates2021filter.qs,
            'calendardates2022filter':calendardates2022filter.qs,
        }


    # we are in term ? week ?
    calendarqs=AcademicCalendar.objects.filter(year=nowyear)

    termnow = "Break"
    term = 0
    week = 0

    for calendardate in calendarqs.values('startdate','finishdate','term'):

        if nowtime > calendardate["startdate"] and nowtime < calendardate["finishdate"]:
            term = calendardate["term"]
            termnow="Term " + term
            weekfloat = (timezone.localtime()-calendardate["startdate"]).days/7

            if len(str(weekfloat)) > 3:

                week=math.ceil((timezone.localtime()-calendardate["startdate"]).days/7)
            else:
                week=math.ceil((timezone.localtime()-calendardate["startdate"]).days/7)+1





    # weather api
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c129cc2419d9b32586f6b3b5fed5810c'
    city = 'Sydney'
    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
    weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }


    context = {
        'current_page': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator,
        "Items": Items,


        'filterpost': noticefilter,
        # 'filtercalendar':calendardatesfilter,
        'posts':noticefilter.qs,

        'calendardates':calendardates,

        'termnow':termnow,
        'term':term,
        'week':week,


        'weather' : weather,
    }


    return render(request,'home/home.html',context)
