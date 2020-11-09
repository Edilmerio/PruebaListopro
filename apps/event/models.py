from django.db import models

class CreatorOrganizer(models.Model):
    idd = models.CharField(null=True, blank=True, max_length=100)
    email = models.EmailField(null=True, blank=True)
    display_name = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.id

class Event(models.Model):
    idd = models.CharField(max_length=100)
    status = models.CharField(null=True, blank=True, max_length=100)
    htmlLink = models.CharField(null=True, blank=True, max_length=100)
    summary = models.CharField(null=True, blank=True, max_length=500)
    start = models.DateTimeField()
    end = models.DateTimeField()
    hangoutLink = models.CharField(null=True, blank=True, max_length=100)
    is_allday = models.BooleanField()
    recurrence = models.CharField(null=True, blank=True, max_length=100)
    creator = models.ForeignKey(CreatorOrganizer, on_delete=models.DO_NOTHING,
                                related_name='creators', null=True, blank=True)
    organizer = models.ForeignKey(CreatorOrganizer, on_delete=models.DO_NOTHING,
                                  related_name='organizers', null=True, blank=True)
    timezone_origin = models.CharField(max_length=100)
