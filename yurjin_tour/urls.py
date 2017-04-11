"""yurjin_tour URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.conf.urls import include, url
from django.contrib import admin
from django.views.i18n import javascript_catalog
#from yurjin_journal.views import TouristList

urlpatterns = [
    url(r'^jsi18n', javascript_catalog, {'packages':('yurjin_journal.apps.YurjinTourConfig',) }),
    
    url(r'^', include('yurjin_main.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^yurjin_journal/', include('yurjin_journal.urls')),
    url(r'^yurjin_reports/', include('yurjin_reports.urls')),    
    
]

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)

# ��� ������ ����������� � ����� ��������� url'� ������ ��� DEBUG = True
urlpatterns += staticfiles_urlpatterns()