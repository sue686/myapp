from django.urls import path

from . import views



urlpatterns = [
    path('docupload/<str:campus>/<str:department>', views.upload, name='docupload'),
    path('doclist/<str:campus>/<str:department>/<str:pagenumber>', views.doclist, name='doclist'), # 上传
    # path('bbidoclist/', views.bbilist),  # 列表
    path('docdownload/<id>', views.download, name='docdownload'),  # 下载
    path('docdelete/<id>/<str:pagenumber>/<str:campus>/<str:department>', views.delete, name='docdelete'),

    path('categoryadd/<str:campus>/<str:department>', views.categoryadd, name='doccategoryadd'),
    path('categoryedit/<id>/<str:pagenumber>/<str:campus>/<str:department>/<str:categoryname>/<str:permission>', views.categoryedit, name='doccategoryedit'),
    path('categorydelete/<id>/<str:pagenumber>/<str:campus>/<str:department>', views.categorydelete, name='doccategorydelete'),



]
