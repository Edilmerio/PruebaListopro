from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse


class Event(TemplateView):
    template_name = 'event/ShowEvent.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)