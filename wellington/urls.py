"""wellington URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from home.views import home_view,home_redirect,releasenotes
from django.urls import include, re_path
# from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('', home_redirect, name='homeredirect'),
    path('home/<str:campus>/<str:year>', home_view, name='home'),
    path('releasenotes', releasenotes, name='releasenotes'),

    path('admin/', admin.site.urls),
    path('it/', include('it.urls')),
    path('docmgt/', include('docmgt.urls')),
    path('blog/', include('blog.urls')),
    path('aduser/', include('aduser.urls')),
    path('ybi/', include('ybielearning.urls')),
    path('bbi/', include('bbielearning.urls')),
    path('smtp/', include('smtp.urls')),

    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/logout.html'), name='logout'),

    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
