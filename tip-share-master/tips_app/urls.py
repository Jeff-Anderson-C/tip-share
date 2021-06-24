from django.urls import path
from django.urls.resolvers import URLPattern
from .import views

urlpatterns = [
    path('', views.index),
    path('profile', views.user),
    path('other_profile', views.other_profile)
]