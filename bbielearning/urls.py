from django.urls import path
from .views import  (
                    bbiSaveuser_View,
                    bbiUpdateusersuspended_View,
                    bbiSavecourses_View,
                    bbiSaveenrolleduser_View,
                    bbihome_view,
                    bbiCourse_view,

                    bbiEnroll_view,
                    bbisync,
                    bbienrolluser_view,
                    bbibulksuspendusers_view,
                    bbiuser_view,
                    bbiuserpriority_view,
                    bbiBBBrecordDelete_View,
                    bbiSaveBBBrecord_View,
                    bbiBBBrecord_View,
                    bbiusertest_view,
                    bbiuserbulkcreate_view,
                    bbiSaveBBBrecord_Backup,
                    bbistudentassigntrainer,
                    bbiusersuspend_view,

)


urlpatterns = [

    path('', bbihome_view, name='bbihome'),

    path('course/', bbiCourse_view, name='bbiCourse'),

    path('users/', bbiuser_view, name='bbiUser'),
    path('user/', bbiusertest_view, name='bbiUsertest'),
    path('bbiupdateusersuspended/', bbiUpdateusersuspended_View,name='bbiUpdateusersuspended'),
    path('userpriority/', bbiuserpriority_view, name='bbiuserpriority'),
    path('userbulkcreate/', bbiuserbulkcreate_view, name='bbiuserbulkcreate'),
    path('usersuspend/', bbiusersuspend_view, name='bbiusersuspend'),

    path('enroll/', bbiEnroll_view.as_view(), name='bbiEnroll'),
    path('sync', bbisync, name='bbisync'),
    path('enrolluser', bbienrolluser_view, name='bbienrolluser'),
    path('bulksuspendusers', bbibulksuspendusers_view, name='bbibulksuspendusers'),
    path('bbistudentassigntrainer', bbistudentassigntrainer, name='bbistudentassigntrainer'),

    path('bbibbbrecordview', bbiBBBrecord_View, name='bbibbbrecordview'),

    path('bbibbbdeleterecord', bbiBBBrecordDelete_View, name='bbiBBBdeleterecord'),


    #path('enroll/suspendenrolluser/<int:courseid>/<int:userid>', suspendenrolluser, name='suspendenrolluser'),

    path('bbisaveusers/', bbiSaveuser_View,name='bbiSaveuser'),
    path('bbisavecourses/', bbiSavecourses_View,name='bbiSavecourses'),
    path('bbisaveenrolleduser/', bbiSaveenrolleduser_View,name='bbiSaveenrolleduser'),
    path('bbiSaveBBBrecord/', bbiSaveBBBrecord_View,name='bbiSaveBBBrecord'),
    path('bbiSaveBBBrecordbackup/', bbiSaveBBBrecord_Backup,name='bbiSaveBBBrecordbackup'),


]
