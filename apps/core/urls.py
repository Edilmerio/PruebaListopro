from django.conf.urls import url

from .views.prueba import Prueba

app_name = 'core'
urlpatterns = [
    url(r'^prueba$', Prueba.as_view(), name='prueba'),
]