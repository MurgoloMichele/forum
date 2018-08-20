from django.urls import path, re_path
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        re_path("boards/(?P<pk>\d+)/$", views.board_topics, name="board_topics"),
        re_path("boards/(?P<pk>\d+)/new/$", views.new_topic, name="new_topic"),
        ]
