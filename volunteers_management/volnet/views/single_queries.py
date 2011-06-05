from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from volnet.models import *
from volnet.views.views import *

def emergency_desc(request):
    #following variables are passed to the template
    user = request.user
    volunteer = None
    member = None
    organization = None
    if user.is_authenticated():
        volunteer = is_volunteer(user)
        member = is_member(user)
        organization = is_organization(user)
    em = None
    enroled = False

    query = request.GET.get("id")
    if query:
        em = Emergency.get(pk=query)
    if is_volunteer(user) and em:
        qset = (Q(user__exact=user))
        vol = Volunteer.objects.filter(qset)
        if vol in em.volunteers:
            enroled = True
    return render_to_response("emergencies/desc.html", locals())

def event(request):
    query = request.GET.get("id")
    event = None
    if query:
        event = Emergency.get(pk=query)
    return render_to_response("events/desc.html", locals())

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
            form = NewEmergencyForm()
        return render_to_response("emergencies/create.html", locals(),
                                  context_instance=RequestContext(request))
    return HttpResponseForbidden()

