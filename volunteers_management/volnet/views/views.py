from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
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
    return HttpResponseRedirect("/emergencies/overview/")

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
    #emergency = None
    #emergency_list = Emergency.objects.filter(active=True)
    if organization:
        qset = (Q(user__exact=user))
        org = Organization.objects.filter(qset)
        qset = (Q(organization__exact=org))
        all_ems = Emergency.objects.filter(qset)
        qset = (Q(active=True))
        ems = all_ems.filter(qset)
        if ems:
            return HttpResponseRedirect("/events/overview/")
        else:
            return HttpResponseRedirect("/emergencies/create/")
    elif member:
        return HttpResponseRedirect("/events/myevents/")
    elif volunteer:
        active_ems = Emergency.objects.filter(Q(active=True))
        vol = Volunteer.objects.filter(Q(user__exact=user))
        for em in active_ems:
            if vol in em.volunteers.all():
                return HttpResponseRedirect("/events/mytasks/")
        return HttpResponseRedirect("/emergencies/overview/")
    elif request.method == "POST":
        form = VolunteerInfoForm(request.POST)
        if form.is_valid():
            form.save_volunteer(user)
            return HttpResponseRedirect("/")
    else:
        form = VolunteerInfoForm()

    return render_to_response("insert_volunteer_info.html", locals(),
                              context_instance=RequestContext(request))

#dalla home (cioe`:da profiles): redirects
#    imbecille -> emergencies/overview/
#    volontario -> se enroled: events/mytask/
#                  else      : emergencies/overview/
#    member  -> events/myevents/
#    organization -> se ha emergenza aperta: events/overview/
#                    altrimenti: emergencies/create/

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
        em = Emergency.objects.get(pk=query)
    if volunteer and em:
        qset = (Q(user__exact=user))
        vol = Volunteer.objects.filter(qset)
        if vol in em.volunteers:
            enroled = True
    return render_to_response("emergencies/desc.html", locals())

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


@login_required
def new_event(request):
    user = request.user
    organization = is_organization(user)
    member = is_member(user)
    volunteer = is_volunteer(user)
    qset = (Q(user__exact=user))
    mem = Member.objects.filter(qset)[0]
    f = create_event_form(mem)
    if request.method == "POST":
        form = f(request.POST)
        if form.is_valid():
            form.save_event()
            return HttpResponseRedirect("/")
    else:
        form = f()
    return render_to_response("events/create.html", locals())

@login_required
def event_desc(request):
    user = request.user
    volunteer = None
    member = None
    organization = None
    if user.is_authenticated():
        volunteer = is_volunteer(user)
        member = is_member(user)
        organization = is_organization(user)
    ev_id  = request.GET.get("id")
    ev = None
    if ev_id:
        ev = Event.objects.filter(Q(pk__exact=ev_id))
        if ev and (volontario or member or organization):
            return render_to_response("events/desc.html", locals())
    return HttpResponseForbidden()

@login_required
def my_events(request):
    user = request.user
    organization = is_organization(user)
    member = is_member(user)
    volunteer = is_volunteer(user)
    qset = (Q(user__exact=user))
    mem = Member.objects.filter(qset)
    if mem:
        evs = Event.objects.filter(member=mem[0])
        return render_to_response("events/myevents.html", locals())
    else:
        return HttpResponseForbidden()

def event_overview(request):
    ems_open = Emergency.objects.filter(Q(active=True))
    result = {}
    for ems in ems_open:
        qset = (Q(emergency__exact=ems))
        result[ems] = Event.objects.filter(qset)
    return render_to_response("events/overview.html", locals())

@login_required
def my_task(request):
    organization = is_organization(user)
    member = is_member(user)
    volunteer = is_volunteer(user)
    qset = (Q(user__exact=user))
    vol = Volunteer.objects.filter(qset)[0]
    evs_open = Event.objects.filter(active=True)
    evs = None
    for ev in evs_open:
        if vol in ev.volunteers.all():
            evs = ev
            break
    if evs:
        return HttpResponseRedirect("/events/description/?id=%d" % evs.pk)
    else:
        return render_to_response("events/mytask.html", locals())

def members_manage(reuqest):
    pass

def emergency_manage(request):
    user = request.user
    volunteer = None
    member = None
    organization = None
    if user.is_authenticated():
        volunteer = is_volunteer(user)
        member = is_member(user)
        organization = is_organization(user)
    if organization:
        org = Organization.objects.filter(Q(user__exact=user))
        org = org[0]
        em_id  = request.GET.get("id")
        if em_id:
            ems = Emergency.objects.filter(Q(pk__exact=em_id))
            if ems:
                em = ems.filter(Q(organization__exact=org))
                if em:
                    return render_to_response("emergencies/manage.html",
                                              locals())
    return HttpResponseForbidden()

def emergency_overview(request):
    user = request.user
    volunteer = None
    member = None
    organization = None
    if user.is_authenticated():
        volunteer = is_volunteer(user)
        member = is_member(user)
        organization = is_organization(user)

    ems_open = Emergency.objects.filter(Q(active=True))
    ems_closed = Emergency.objects.filter(Q(active=False))
    return render_to_response("emergencies/overview.html", locals())

@login_required
def emergency_join(request):
    if user.is_authenticated():
        if is_volunteer(user):
            active_ems = Emergency.objects.filter(Q(active=True))
            vol = Volunteer.objects.filter(Q(user__exact=user))
            free_vol=True
            for em in active_ems:
                if not(vol in em.volunteers):
                    free_vol=False
                    break
            if free_vol:
                em_id  = request.GET.get("id")
                if em_id:
                    em = Emergency.objects.filter(Q(pk__exact=em_id))
                    if em:
                        em = em[0]
                        em.volunteers.add(vol)
    return HttpResponseForbidden()

@login_required
def emergency_leave(request):
    if user.is_authenticated():
        if is_volunteer(user):
            vol = Volunteer.objects.filter(Q(user__exact=user))
            em_id  = request.GET.get("id")
            if em_id:
                em = Emergency.objects.filter(Q(pk__exact=em_id))
                if em:
                    em = em[0]
                    em.volunteers.remove(vol)
    return HttpResponseForbidden()


#non e` una view
def closeevent(event):
    event.active = False
    event.save()
    for vol in event.volunteers.all():
        vol.available = True
        vol.save()

@login_required
def event_close(request):
    user = request.user
    organization = is_organization(user)
    member = is_member(user)
    volunteer = is_volunteer(user)
    qset = (Q(user__exact=user))
    mem = Members.objects.filter(qset)[0]
    #evs_open = Event.objects.filter(active=True)
    ev_id = request.GET.get("id")
    if ev_id:
        ev = Event.objects.get(pk=ev_id)
        if ev and (mem in ev.member.all()):
            closeevent(ev)
            return HttpResponseRedirect("/")
    return HttpResponseForbidden()

@login_required
def emergency_close(request):
    user = request.user
    organization = is_organization(user)
    member = is_member(user)
    volunteer = is_volunteer(user)
    qset = (Q(user__exact=user))
    org = Organization.objects.filter(qset)
    evs_open = Event.objects.filter(active=True)
    query = request.GET.get("id")
    if query and org:
        em = Emergency.objects.get(pk=query)[0]
        if em:
            evs = evs_open.filter(emergency__exact=em)
            for ev in evs:
                closeevent(ev)
                return HttpRedirectResponse("/")
    return HttpResponseForbidden()

def call_volunteers(request):
    pass

def volunteer_desc(request, query):
    user = request.user
    organization = is_organization(user)
    member = is_member(user)
    volunteer = is_volunteer(user)
    vol = None
    comments = None
    form = None
    if query:
        u = User.objects.get(pk=query)
        vol = Volunteer.objects.filter(user__exact=u)[0]
        comments = VolunteerComment.objects.filter(volunteer=vol)
        if request.method == "POST":
            form = VolunteerCommentForm(request.POST)
            if form.is_valid():
                form.save_comment(user, vol)
        else:
            form = VolunteerCommentForm()
    return render_to_response("volunteers/desc.html", locals(),
                              context_instance=RequestContext(request))
