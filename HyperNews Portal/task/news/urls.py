from django.urls import path
from django.urls import re_path
from news.views import CreateView, NewsView, MainView
from . import views

urlpatterns = [
    path('', views.soon),
    path('news/', MainView.as_view()),
    path('news/create/', CreateView.as_view()),
    re_path(r'news/(?P<news_id>[0-9]+)/$', NewsView.as_view()),
]
