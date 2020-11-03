import os
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from config import settings
from core.utils import write_log
from ..models import Event

def get_events_json(request):
    """
    api  return events between satrt and end datetime
    parms start an end datetime isoformat
    """
    try:
        start_req = datetime.fromisoformat(request.GET['start'])
        end_req = datetime.fromisoformat(request.GET['end'])
    except (KeyError, ValueError):
        write_log('Do not exist or do not have isoformat start or end date')
        return JsonResponse([], safe=False)

    # get events without recurrence
    queryset = Event.objects.filter((Q(start__gte=start_req) & Q(start__lte=end_req)) |
                                    (Q(end__gte=start_req) & Q(end__lte=end_req)))
    queryset = queryset.filter(recurrence=None)
    events_show = []
    for q in queryset:
        if q.is_allday:
            start = q.start.date()
            end = q.end.date()
        else:
            start = q.start
            end = q.end
        events_show.append({'id': q.idd, 'status': q.status, 'htmlLink': q.htmlLink,
                            'summary': q.summary, 'title': q.summary, 'start': start,
                            'end': end, 'hangoutLink': q.hangoutLink,
                            'creator': {'email': q.creator.email,  'displayName': q.creator.display_name},
                            'organizer': {'email': q.organizer.email, 'displayName': q.organizer.display_name}})
    return JsonResponse(events_show, safe=False)