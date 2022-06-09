from django.urls import path
from zusers import views

urlpatterns=[
    path('actionRegister', views.actionRegisterView),
    path('actionLogin', views.actionLoginView),
    path('checkIsLogin',views.checkIsLogin),
    path('getUserName',views.getUserName),
]