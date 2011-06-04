from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from volnet.models import *

def emergency(request):
    query = request.GET.get("emergency")
    em = None
    if query:
        em = Emergency.get(pk=query)
    render_to_response("emergencies/desc.html", locals())

def event(request):
    query = request.GET.get("event")
    event = None
    if query:
        event = Emergency.get(pk=query)
    render_to_response("events/desc.html", locals())
