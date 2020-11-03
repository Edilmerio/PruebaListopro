from django.conf.urls import url

from .views.show_event import Event
from .api.save_events import save_events_from_json_file
from .api.get_events import get_events_json
app_name = 'core'
urlpatterns = [
    url(r'^show_events$', Event.as_view(), name='show_events'),
    url(r'^save_events_from_json_file$', save_events_from_json_file, name='save_events_from_json_file'),
    url(r'^get_events$', get_events_json, name='get_events'),
]