import os

from django.http import HttpResponse, JsonResponse

from config import settings
from core.utils import read_json_file_convert_to_python
from ..events import Events

def save_events_from_json_file(request):
    """
    api  for save or update events from json file (events.json)
    """
    file = os.path.join(settings.BASE_DIR, 'events.json')
    if not os.path.isfile(file):
        return JsonResponse({'text': 'No file events.json',
                             'title': 'Load Events', 'type': 'info'})
    calendar = read_json_file_convert_to_python(file)
    events = calendar.get('items', [])
    result = Events.update_bd(events, calendar['timeZone'])
    return JsonResponse({'text': 'Insert: {}, Update: {}, Error: {}'.format(result[0], result[1], result[2]),
                         'title': 'Load Events', 'type': 'info'})