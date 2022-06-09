from django.urls import path
from zcodes import views

urlpatterns = [
    path('addProject', views.addProjectView),
    path('getAllProjects', views.getAllProjectsView),
    path('getProject', views.getProjectView),
]
