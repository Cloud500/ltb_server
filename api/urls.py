from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('fetch_new_books', views.FetchNewBook.as_view(), name='fetch_new_books'),
]
