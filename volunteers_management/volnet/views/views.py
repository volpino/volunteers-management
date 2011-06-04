from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from volnet.models import *
from forms import *
from django.template import RequestContext


def home(request):
    #chiama funzione che assegna i volontari
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect("/accounts/profile/")
    return render_to_response("base.html")
#dalla home (cioe`:da profiles): redirects
#    imbecille -> emergencies/overview/
#    volontario -> se enroled: events/mytask/
#                  else      : emergencies/overview/
#    member  -> events/myevents/
#    organization -> se ha emergenza aperta: events/overview/
#                    altrimenti: emergencies/create/

def about(request):
    user = request.user
    volunteer = None
    member = None
    organization = None
    if user.is_authenticated():
        volunteer = is_volunteer(user)
        member = is_member(user)
        organization = is_organization(user)
    return render_to_response("about.html", locals())

def contact(request):
    user = request.user
    volunteer = None
    member = None
    organization = None
    if user.is_authenticated():
        volunteer = is_volunteer(user)
        member = is_member(user)
        organization = is_organization(user)
    return render_to_response("contact.html", locals())

def is_member(user):
    qset = (Q(user__exact=user))
    member = Member.objects.filter(qset)
    if member:
        return True
    else:
        return False

def is_organization(user):
    qset = (Q(user__exact=user))
    member = Organization.objects.filter(qset)
    if member:
        return True
    else:
        return False

def is_volunteer(user):
    qset = (Q(user__exact=user))
    member = Volunteer.objects.filter(qset)
    if member:
        return True
    else:
        return False

@login_required
def profile(request):
    user = request.user
    organization = is_organization(user)
    member = is_member(user)
    volunteer = is_volunteer(user)
    qset = (Q(user__exact=user))
    vol = Volunteer.objects.filter(qset)
    emergency = None
    emergency_list = Emergency.objects.filter(active=True)
    if organization or member or volunteer:
        for em in emergency_list:
            if vol in em.volunteers.all():
                emergency = em
                break
        return render_to_response("home.html", locals())
    if request.method == "POST":
        form = VolunteerInfoForm(request.POST)
        if form.is_valid():
            form.save_volunteer(user)
    else:
        form = VolunteerInfoForm()

    return render_to_response("insert_volunteer_info.html", locals(),
                              context_instance=RequestContext(request))


def new_event(request):
    qset = (Q(user__exact=user))
    member = Member.objects.filter(qset)
    f = createNewEventForm(member)
    if request.method == "POST":
        form = f(request.POST)
        if form.is_valid():
            form.save_events(user)
    else:
        form = f()
