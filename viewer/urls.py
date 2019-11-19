from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.projects, name='projects_all'),
    path('id/<int:project_pk>', views.detail, name='project_details'),
    re_path(r'^teams/$', views.teams, name='teams_all'),
    re_path(r'^locations/$', views.locations, name='locations_all')
    ]