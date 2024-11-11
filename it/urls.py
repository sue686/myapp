from django.urls import path
from .views import  IThome_view



urlpatterns = [

    path('', IThome_view, name='ithome'),

]
