from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^registration$', views.registration),
  url(r'^login$', views.login),
  url(r'^successlog$', views.successlog),
  url(r'^successreg$', views.successreg),
  url(r'^logout$', views.logout),
  url(r'^fave/(?P<id>\d+)$', views.fave),
  url(r'^remove/(?P<id>\d+)$', views.remove),
  url(r'^new$', views.new),
  url(r'^users/(?P<id>\d+)$', views.users),
  url(r'^main$', views.main),
  # url(r'^main/(?P<id>\d+)$', views.main),
]
