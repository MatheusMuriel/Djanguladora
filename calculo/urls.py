from django.conf.urls import url
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^bissecao/$', bissecao, name='bissecao'),
    url(r'^gauss/$', gauss, name='gauss'),
]