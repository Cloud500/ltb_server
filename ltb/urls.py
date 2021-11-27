from django.urls import path
from . import views

app_name = 'ltb'
urlpatterns = [
    # path('all', views.book_list_all, name='book_list_all'),
    path('<str:s_type>', views.book_list_type, name='book_list_type'),
    path('detail/<str:slug>',
         views.book_detail,
         name='book_detail'),
]
