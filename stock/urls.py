from django.urls import path
from . import views

app_name = 'stock'
urlpatterns = [
    path('<str:s_type>', views.QuantList.as_view(), name='quant_list_type'),
    path('book/add', views.AddBook.as_view(), name='add_book_form'),
    path('book/find', views.FindNumber.as_view(), name='find_number')
]
