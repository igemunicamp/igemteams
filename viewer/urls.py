from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.projects, name='projects_all'),
    path('projects/id/<int:project_pk>', views.detail, name='project_details')
    ]