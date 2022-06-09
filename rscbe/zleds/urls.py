from django.urls import path
from zleds import views

urlpatterns=[
    path('setBrightness', views.setBrightness),
    path('setRGBLED', views.setRGBLED),
    path('clearGPIO', views.clearGPIO),
    path('setWS2812', views.setWS2812),
]