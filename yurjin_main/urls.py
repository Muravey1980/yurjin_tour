from django.conf.urls import url

from yurjin_main.views import MainPageView

app_name = 'yurjin_main'
urlpatterns = [
  #url(r'^$', index, name = "index"),
  url(r'^$', MainPageView.as_view(), name = "index"),
]
