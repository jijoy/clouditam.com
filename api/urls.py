from django.conf.urls import include, url
from rest_framework import routers
from api.views import UserCreateView, UserLoginView



urlpatterns = [
    url(r'^accounts/create/$', UserCreateView.as_view()),
    url(r'^accounts/login/$', UserLoginView.as_view()),
]
