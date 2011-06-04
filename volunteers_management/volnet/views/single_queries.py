from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from volnet.models import *
from volnet.views.views import *

def emergency(request):
    #following variables are passed to the template
    user = request.user
    organization = is_organization(user)
    member = is_member(user)
    volunteer = is_volunteer(user):
    em = None
    enroled = False
    
    query = request.GET.get("emergency")
    if query:
        em = Emergency.get(pk=query)
    if is_volunteer(user) and em:
        qset = (Q(user__exact=user))
        vol = Volunteer.objects.filter(qset)
        if vol in em.volunteers:
            enroled = True
    render_to_response("emergencies/desc.html", locals())

def event(request):
    query = request.GET.get("event")
    event = None
    if query:
        event = Emergency.get(pk=query)
    render_to_response("events/desc.html", locals())

@login_required
def new_emergency(request):
    user = request.user
    organization = is_organization(user)
    member = is_member(user)
    volunteer = is_volunteer(user)
    if organization:
        if request.method == "POST":
            form = NewEmergencyForm(request.POST)
            if form.is_valid():
                form.save_emergency(user)
        else:
            form = VolunteerInfoForm()
        return render_to_response("new_emergency.html", locals(),
                                  context_instance=RequestContext(request))


