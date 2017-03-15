from django.conf.urls import url
from web.views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]