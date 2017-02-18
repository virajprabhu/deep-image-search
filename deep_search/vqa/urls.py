from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.vqa, name='vqa_api'),
]
