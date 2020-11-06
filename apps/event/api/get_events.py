from datetime import datetime, timedelta
from copy import copy

from django.http import JsonResponse
from django.db.models import Q
from dateutil.parser import parse
from dateutil import tz
from dateutil.rrule import rrulestr

from core.utils import write_log
from ..models import Event
from config import settings

def get_events_json(request):
    """
    api  return events between start and end datetime
    parms start an end datetime isoformat
    """
    try:
        start_req = parse(request.GET['start'])
        end_req = parse(request.GET['end'])
    except (KeyError, ValueError):
        write_log('Do not exist or do not have format start or end date')
        return JsonResponse([], safe=False)
    if start_req.tzinfo is None or start_req.tzinfo.utcoffset(start_req) is None:
        tz_req = tz.gettz(request.GET['timeZone'])
        start_req = start_req.astimezone(tz=tz_req)
        end_req = end_req.astimezone(tz=tz_req)

    single_events = __process_single_events(start_req, end_req)
    recurring_events = __process_recurring_events(start_req, end_req)

    return JsonResponse(single_events + recurring_events, safe=False)


def __process_single_events(start, end):
    """
    Process single events
    """
    # get events without recurrence
    # queryset = Event.objects.filter((Q(start__gte=start) & Q(start__lte=end)) |
    #                                 (Q(end__gte=start) & Q(end__lte=end)))
    queryset = Event.objects.filter(recurrence=None)
    single_events = []
    for q in queryset:
        v = __create_dict_for_fullcalendar(q, start, end)
        if v:
            single_events.append(v)
    return single_events


def __create_dict_for_fullcalendar(q, start1, end1):
    """
    create dict for fullcalendar from events
    q is events instance
    """
    if (start1 <= q.start <= end1) | (start1 <= q.end <= end1):
        if q.is_allday:
            start = q.start.date()
            end = q.end.date()
        else:
            start = q.start.astimezone(tz=start1.tzinfo)
            end = q.end.astimezone(tz=start1.tzinfo)
        return {'id': q.idd, 'status': q.status, 'htmlLink': q.htmlLink,
                'summary': q.summary, 'title': q.summary, 'start': start,
                'end': end, 'hangoutLink': q.hangoutLink,
                'creator': {'email': q.creator.email,  'displayName': q.creator.display_name},
                'organizer': {'email': q.organizer.email, 'displayName': q.organizer.display_name}}
    return None


def __process_recurring_events(start, end):
    """
    process recurring events
    """
    recurring_events = []
    queryset = Event.objects.exclude(recurrence=None)
    for q in queryset:
        recurring_events.extend(__create_events_from_recurring_event(q, start, end))
    return recurring_events


def __create_events_from_recurring_event(ev, start, end):
    """
    Do list with events from recurring event between start and end date or datetime
    """
    recurrence = eval(ev.recurrence)
    # if recurrence do not have UNTIL, end_recurrence = end
    rrule_string = recurrence['RRULE']
    if 'UNTIL' not in rrule_string:
        end_recurrence = end
        string_recurrence = rrule_string
    else:
        aux = rrule_string[rrule_string.find('UNTIL=') + len('UNTIL='):]
        ind = aux.find(';')
        # if ind == -1 no find
        if ind == -1:
            until_string = aux
        else:
            until_string = aux[:ind]
        until = parse(until_string)
        localtz = tz.gettz(settings.TIME_ZONE)
        if until.tzinfo is None or until.tzinfo.utcoffset(until) is None:
            # is date naive
            until = datetime(year=until.year, month=until.month, day=until.day, tzinfo=localtz) + timedelta(days=1)
        string_recurrence = rrule_string.replace('UNTIL='+until_string+';', '')
        # if until gt end, end_recurrence = end
        if until > end:
            end_recurrence = end
        # if until lte end, end_recurrence = until
        else:
            end_recurrence = until
    # replace BYDAY for BYWEEKDAY
    string_recurrence = string_recurrence.replace('BYDAY', 'BYWEEKDAY')
    string_recurrence = string_recurrence + ';UNTIL={}'.format(end_recurrence.strftime('%Y%m%dT%H%M%S%z'))

    delta_time = ev.end - ev.start
    events_aux = []
    for r in list(rrulestr(string_recurrence, dtstart=ev.start)):
        copy_ev = copy(ev)
        copy_ev.start = r
        copy_ev.end = r + delta_time
        v = __create_dict_for_fullcalendar(copy_ev, start, end)
        if v:
            events_aux.append(v)

    return events_aux
