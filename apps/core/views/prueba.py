import os

from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse

from config import settings
from ..utils import read_json_file_convert_to_python
from event.events import Events

class Prueba(TemplateView):
    template_name = 'core/Layout.html'

    def get(self, request, *args, **kwargs):
        absdir = os.path.join(settings.BASE_DIR, 'events.json')
        Events.update_bd({})
        a = Events.idds_events
        return render(request, self.template_name)
