from django.conf.urls import url

from .views.login import Login

app_name = 'auth_sisop'

urlpatterns = [
    url(r'^login$', Login.as_view(), name='login'),
]