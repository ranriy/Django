from django.conf.urls import url
from . import views           

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$',views.login),
    url(r'^register$',views.register),
    url(r'^display$',views.display),
    url(r'^add/(?P<id>\d+)$',views.add),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^logout$', views.logout),
    url(r'^view/(?P<id>\d+)$', views.viewpage)
]