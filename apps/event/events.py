from datetime import datetime, date

import pytz
from dateutil import tz
from django.db import transaction
from django.db import DatabaseError

from .models import Event, CreatorOrganizer
from core.utils import write_log
from config import settings

class Events:

    @staticmethod
    def update_bd(events, timezone_calendar):
        """
        update or create events in bd
        """
        event_error = 0
        events_update = 0
        events_create = 0

        for event in events:
            creator, organizer = Events.__build_creator_organizer(event)
            d = Events.__build_start_end_is_allday(event, timezone_calendar)
            if not d:
                # event with error in date
                event_error += 1
                continue
            recurrence = Events.__build_recurrence(event)
            # get id for creator the this event
            try:
                id_creator = Event.objects.get(idd=event['id']).creator.id
            except Event.DoesNotExist:
                id_creator = None
            # get id for organizer the this event
            try:
                id_organizer = Event.objects.get(idd=event['id']).organizer.id
            except Event.DoesNotExist:
                id_organizer = None

            default = {}
            simple_fields = ['status', 'htmlLink', 'summary', 'hangoutLink']
            for f in simple_fields:
                default[f] = event.get(f, None)
            try:
                with transaction.atomic():
                    creator_bd = CreatorOrganizer.objects.update_or_create(defaults={'idd': creator.idd, 'email': creator.email,
                                                                                     'display_name': creator.display_name}, id=id_creator)

                    organizer_bd = CreatorOrganizer.objects.update_or_create(defaults={'idd': organizer.idd, 'email': organizer.email,
                                                                                       'display_name': organizer.display_name},
                                                                             id=id_organizer)

                    default.update({'start': d[0], 'end': d[1], 'is_allday': d[2], 'recurrence': recurrence, 'timezone_origin': d[3],
                                    'creator': creator_bd[0], 'organizer': organizer_bd[0]})

                    result = Event.objects.update_or_create(defaults=default, idd=event['id'])
            except DatabaseError:
                event_error += 1
                continue
            if result[1]:
                events_create += 1
            else:
                events_update += 1
        return events_create, events_update, event_error

    @staticmethod
    def __build_creator_organizer(event):
        """
        build creator and organizer objects from event
        """
        creator = event.get('creator', None)
        organizer = event.get('organizer', None)
        if creator:
            creator = CreatorOrganizer(idd=creator.get('id', None), email=creator.get('email', None),
                                       display_name=creator.get('displayName', None))
        if organizer:
            organizer = CreatorOrganizer(idd=organizer.get('id', None), email=organizer.get('email', None),
                                         display_name=organizer.get('displayName', None))
        return creator, organizer

    @staticmethod
    def __build_start_end_is_allday(event, tzcalendar):
        """
        build start, end and is_allday
        """
        localtz = tz.gettz(settings.TIME_ZONE)
        try:
            start_string = event['start'].get('date', None)
            if start_string:
                # start is type date
                is_allday = True
                date_start = date.fromisoformat(start_string)
                start = datetime(year=date_start.year, month=date_start.month, day=date_start.day, tzinfo=localtz)
                # when start is type date end too
                date_end = date.fromisoformat(event['end'].get('date'))
                end = datetime(year=date_end.year, month=date_end.month, day=date_end.day, tzinfo=localtz)
            else:
                # if start is not type date, the type is datetime
                is_allday = False
                start_string = event['start'].get('dateTime')
                # when start is type datetime end too
                end_string = event['end'].get('dateTime')
                start = datetime.fromisoformat(start_string)
                end = datetime.fromisoformat(end_string)

            tz_event = event['start'].get('timeZone', None)
            tz_event = tz_event if tz_event else tzcalendar
            return start, end, is_allday, tz_event
        except KeyError:
            write_log('Error to convert string start or end to date o datetime, event: '.format(event['id']))
            return []

    @staticmethod
    def __build_recurrence(event):
        """
        return string with all property recurrence in string
        dictionary {RRULE: string RRULE, RDATE: string RDATE, EXDATE: string EXDATE}
        """
        array_recurrence = event.get('recurrence', None)
        if not array_recurrence:
            return None
        dict_rrule = {}
        for el in array_recurrence:
            if 'RRULE' in el:
                dict_rrule['RRULE'] = el
                continue
            if 'RDATE' in el:
                dict_rrule['RDATE'] = el
                continue
            if 'EXDATE' in el:
                dict_rrule['EXDATE'] = el
                continue
        return str(dict_rrule)



