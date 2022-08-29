from django.urls import path
from . import views

app_name = 'person'
urlpatterns = [
    path('real/', views.RealPersonList.as_view(), name='real_person_list'),
    path('fictional/', views.FictionalPersonList.as_view(), name='fictional_person_list'),
    path('real/<str:slug>',
         views.RealPersonDetail.as_view(),
         name='real_person_detail'),
    path('fictional/<str:slug>',
         views.FictionalPersonDetail.as_view(),
         name='fictional_person_detail')
]
