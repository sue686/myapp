from django.urls import path

from . import views



urlpatterns = [

    path('studentmgt/', views.studentmgtview, name='studentmgtview'),
    path('changecomputerpwview/<str:samaccountname>/<str:password>/', views.changecomputerpwview, name='changecomputerpwview'),
    path('receive-json/', views.receive_json, name='receive_json'),
    path('create_students_in_ad/', views.create_students_in_ad, name='create_students_in_ad'),
    path('create_students_in_moodle/', views.create_students_in_moodle, name='create_students_in_moodle'),
    path('change_moodle_user_password/<str:campus>/<str:samaccountname>/<str:password>/', views.change_moodle_user_password, name='change_moodle_user_password'),
]

