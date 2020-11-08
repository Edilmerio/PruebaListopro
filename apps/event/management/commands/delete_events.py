from django.core.management.base import BaseCommand, CommandError
from ...models import Event, CreatorOrganizer


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.delete_all_events_and_creator_organizer()

    def delete_all_events_and_creator_organizer(self):
        """
        delete all events and all creatorOrganizer
        """
        Event.objects.all().delete()
        print('Events delete success')
        CreatorOrganizer.objects.all().delete()
        print('Creator and Organizer delete success')
