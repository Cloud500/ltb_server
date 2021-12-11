from django.urls import path
from . import views

app_name = 'ltb'
urlpatterns = [
    path('<str:s_type>', views.LTBList.as_view(), name='ltb_list'),
    path('detail/<str:slug>',
         views.LTBDetail.as_view(),
         name='book_detail')
]
