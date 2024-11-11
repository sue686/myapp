from django.shortcuts import render
from .forms import ArticleAddForm,ArticleEditForm
from .models import Post
from home.models import EmailAddress
from .filters import PostFilter
from datetime import datetime
from django.utils import timezone
from home.views import paginate
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.
def param(campus,department):
    base_template="home/" + campus +"base.html"
    if campus == "weg":
        urlhome = "home"
    else:
        urlhome = campus + "home"
    return base_template,urlhome


def articlelist(request,campus,department):

    base_template,urlhome=param(campus,department)


    # form = ArticleListForm()

    # qs = Post.objects.all().order_by('-postdate')
    f = PostFilter(request.GET, queryset=Post.objects.all())



    context = {

        'posts': f.qs,
        'filter':f,
        'urlhome' :urlhome,
        'base_template':base_template
    }

    return render(request, "blog/articlelist.html", context)


def articledetail(request,id,campus,department):

    base_template,urlhome=param(campus,department)


    # form = ArticleListForm()

    # qs = Post.objects.all().order_by('-postdate')
    f = PostFilter(request.GET, queryset=Post.objects.filter(id=id))



    context = {

        'posts': f.qs,
        'urlhome' :urlhome,
        'campus':campus,
        'department':department,
        'base_template':base_template
    }

    return render(request, "blog/articledetail.html", context)


@login_required
def articlemgt(request,campus,department,pagenumber):

    # base_template="home/" + campus +"base.html"

    base_template,urlhome=param(campus,department)
    # qs = Post.objects.all().order_by('-postdate')
    f = PostFilter(request.GET, queryset=Post.objects.filter(department=department,campus=campus).order_by('-updatedate'))

    paginator,current_page,is_paginated,Items = paginate(f.qs,request,25,pagenumber)

    context = {
        'current_page': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator,
        "Items": Items,
        'filter': f,
        'campus':campus,
        'department':department,
        'base_template':base_template,
        'urlhome' :urlhome,
    }

    return render(request, "blog/articlemgt.html", context)

@login_required
def articleadd(request,campus,department):
    base_template,urlhome=param(campus,department)
    if request.method == 'POST':

        form = ArticleAddForm(request.POST)
        if form.is_valid():

            # form.save(commit=True)

            new_form = form.save(commit=False)
            new_form.department = department
            new_form.campus = campus
            new_form.postdate = timezone.localtime()
            new_form.updatedate = timezone.localtime()
            new_form.postuser = request.user.username
            new_form.save()
            form.save_m2m()

            title = form.cleaned_data.get('title')
            ISemail = request.POST.get('email')
            emailcontent = "Hi, there is a new notice, please go to http://intranet.wellingtonedu.com.au/blog/articledetail/"+str(new_form.pk)+"/"+campus+"/"+department + " to find details."
            emailaddresses = EmailAddress.objects.filter(groupname_id = 1).values_list('email', flat=True).distinct()
            if ISemail:

                send_mail(title,emailcontent , 'intranet@york.edu.au', emailaddresses)

            IStop = request.POST.get('top')

            return HttpResponseRedirect(reverse('articlemgt', kwargs={'campus': campus,'department':department,'pagenumber':1}))
            # return articlemgt(request,campus,department)

        else:
            return HttpResponseRedirect(reverse('articlemgt', kwargs={'campus': campus,'department':department,'pagenumber':1}))
    else:
        form = ArticleAddForm(request.POST or None)
        context = {

            'form': form,
            'campus':campus,
            'department':department,
            'base_template':base_template,
            'urlhome' :urlhome,
        }

        return render(request, "blog/articleadd.html", context)

@login_required
def articleedit(request,id,campus,department):

    base_template,urlhome=param(campus,department)

    post = Post.objects.get(id=id)


    if request.method == 'POST':
        form = ArticleEditForm(request.POST, instance=post)

        if form.is_valid():

            # form.save(commit=True)
            new_form = form.save(commit=False)
            new_form.updatedate = timezone.localtime()
            new_form.updateuser = request.user.username
            new_form.save()
            form.save_m2m()

            title = form.cleaned_data.get('title')
            ISemail = form.cleaned_data.get('email')
            # if ISemail:
            #     send_mail(title, 'Hi, There is a new Notice, please go to http://intranet.wellingtonedu.com.au', 'it@york.edu.au', ['it@york.edu.au'])

            IStop = request.POST.get('top')

            return HttpResponseRedirect(reverse('articlemgt', kwargs={'campus': campus,'department':department,'pagenumber':1}))

        else:
            return HttpResponseRedirect(reverse('articlemgt', kwargs={'campus': campus,'department':department,'pagenumber':1}))
    else:
        form = ArticleEditForm(instance=post)
        context = {

            'form': form,
            'base_template':base_template,
            'campus':campus,
            'department':department,
            'urlhome' :urlhome,
        }

        return render(request, "blog/articleedit.html", context)

@login_required
def articledelete(request, id,campus,department, pagenumber):

    postitem = Post.objects.get(id=id)
    postitem.delete()

    return HttpResponseRedirect(reverse('articlemgt', kwargs={'campus': campus,'department':department,'pagenumber':pagenumber}))
