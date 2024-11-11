from django.urls import path
from .views import  (
                    YbiSaveuser_View,
                    YbiUpdateusersuspended_View,
                    YbiSavecourses_View,
                    YbiSaveenrolleduser_View,
                    Ybihome_view,
                    Course_view,

                    Enroll_view,
                    sync,
                    enrolluser_view,
                    bulksuspendusers_view,
                    user_view,
                    YbiSaveBBBrecord_View,
                    YbiBBBrecord_View,
                    YbiBBBrecordDelete_View,
                    ybiuserbulkcreate_view,
                    ybiuserpriority_view,
                    ybiusersuspend_view,

)


urlpatterns = [

    path('', Ybihome_view, name='ybihome'),
    path('course/', Course_view, name='Course'),
    path('users/', user_view, name='User'),
    path('enroll/', Enroll_view.as_view(), name='Enroll'),
    path('sync', sync, name='sync'),
    path('enrolluser', enrolluser_view, name='enrolluser'),
    path('bulksuspendusers', bulksuspendusers_view, name='bulksuspendusers'),
    path('userpriority/', ybiuserpriority_view, name='ybiuserpriority'),
    path('usersuspend/', ybiusersuspend_view, name='ybiusersuspend'),

    path('ybibbbrecordview', YbiBBBrecord_View, name='ybibbbrecordview'),
    path('ybibbbdeleterecord', YbiBBBrecordDelete_View, name='ybiBBBdeleterecord'),


    #path('enroll/suspendenrolluser/<int:courseid>/<int:userid>', suspendenrolluser, name='suspendenrolluser'),

    path('ybisaveusers/', YbiSaveuser_View,name='YbiSaveuser'),
    path('userbulkcreate/', ybiuserbulkcreate_view, name='ybiuserbulkcreate'),

    path('ybiupdateusersuspended/', YbiUpdateusersuspended_View,name='YbiUpdateusersuspended'),

    path('ybisavecourses/', YbiSavecourses_View,name='YbiSavecourses'),

    path('ybisaveenrolleduser/', YbiSaveenrolleduser_View,name='YbiSaveenrolleduser'),
    path('ybiSaveBBBrecord/', YbiSaveBBBrecord_View,name='ybiSaveBBBrecord'),


]
