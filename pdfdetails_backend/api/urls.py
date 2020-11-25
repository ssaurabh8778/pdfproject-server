from django.urls import path
from . import views

urlpatterns = [
    path('check', views.check, name='check'),
    path('getFontData', views.getFontData, name='getFontData'),
]