from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.image_captioning_list, name='image_captioning_list'),
    url(r'^(?P<pk>[0-9]+)$', views.image_captioning_detail, name='image_captioning_detail'),
]
