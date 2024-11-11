from django.urls import path

from . import views



urlpatterns = [
    path('articlemgt/<str:campus>/<str:department>/<str:pagenumber>', views.articlemgt, name='articlemgt'),
    # path('articletop/<id>/<str:campus>/<str:department>', views.articletop, name='articletop'),
    # path('articlemgtbypagenumber/<str:campus>/<str:department>/<str:pagenumber>', views.articlemgtbypagenumber, name='articlemgtbypagenumber'),
    path('articlelist/<str:campus>/<str:department>', views.articlelist, name='articlelist'),
    path('articledetail/<id>/<str:campus>/<str:department>', views.articledetail, name='articledetail'),
    path('articleadd/<str:campus>/<str:department>', views.articleadd, name='articleadd'),
    path('articleedit/<id>/<str:campus>/<str:department>', views.articleedit, name='articleedit'),
    path('articledelete/<id>/<str:campus>/<str:department>/<pagenumber>', views.articledelete, name='articledelete'),

]
