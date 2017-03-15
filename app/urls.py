"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from app import settings
from ecommerce.views import test
from web.views import SignInView, LogoutView
from web.views import SignUpView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('dashboard.urls')),
    url('^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^signin/$', SignInView.as_view(), name='signin'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^test/$', test)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    features = [
        url(r'^api/v1/', include('api.urls')),
    ]
    urlpatterns += features
MAINTENANCE = False
if MAINTENANCE:
    urlpatterns += [
    url(r'^$', TemplateView.as_view(template_name='web/maintenance.html'), name="index"),
    url(r'^demo/', include('web.urls')),
]
if not MAINTENANCE:
    urlpatterns += [
        url(r'^', include('web.urls')),
        ]


handler400 = 'web.views.badRequestView.'
handler403 = 'web.views.forbiddenView'
handler404 = 'web.views.notFoundView'
handler500 = 'web.views.serverErrorView'
