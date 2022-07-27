from django.urls import path
from . import views

app_name = 'story'
urlpatterns = [
    path('', views.StoryList.as_view(), name='story_list'),
    path('<str:slug>',
         views.StoryDetail.as_view(),
         name='story_detail'),
]
