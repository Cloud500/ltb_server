from django.urls import path
from . import views

app_name = 'stock'
urlpatterns = [
    # path('all', views.book_list_all, name='book_list_all'),
    path('<str:s_type>', views.quant_list_type, name='quant_list_type'),
    path('book/add', views.add_book, name='add_book_form'),
]
